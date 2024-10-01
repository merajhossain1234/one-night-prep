# my_app/views.py
import os
import google.generativeai as gmini
from django.http import JsonResponse
from django.views import View
from .embedding_service import generate_embedding, compute_similarity
from session.models import Document,Youtube, KnowledgeBase,Session,SessionMember
import fitz

class PDFUploadView(View):
    def post(self, request):
        file = request.FILES['pdf_file']
        title=request.data.get('title')

        # Check if the file is a PDF
        if not file.name.endswith(".pdf"):
            return JsonResponse({'error': 'Only PDF files are allowed.'}, status=400)
        
        session=Session.objects.get(creator=request.user)
        
        # Check if the user is part of the session
        if not session:
            return JsonResponse({'error': 'You are not a member of this session.'}, status=403)
        
        # Create the document record
        pdf_document = Document.objects.create(
            type="pdf",
            title=title,
            pdf_file=file,
            session=session, 
            user=request.user
        )

        # Open the PDF and extract text per page
        with fitz.open(file) as pdf:
            for page_num in range(len(pdf)):
                page = pdf.load_page(page_num)
                text = page.get_text("text")

                # Generate embedding for the page text
                embedding = generate_embedding(text)

                # Save each page with text and embedding in the KnowledgeBase
                knowledge_base_entry, created = KnowledgeBase.objects.update_or_create(
                    object_id=pdf_document.id,
                    page_no=page_num + 1,
                    defaults={
                        'type': pdf_document.type,
                        'text': text,
                        'vector': embedding,
                        'session': session
                    })

        return JsonResponse({'message': 'PDF uploaded and processed successfully'})

class PDFQueryView(View):
    def post(self, request, document_id):
        question = request.POST.get('question')

        # Generate embedding for the user's query
        query_embedding = generate_embedding(question)

        # Retrieve all the pages for the document from the KnowledgeBase
        pages = KnowledgeBase.objects.filter(object_id=document_id).order_by('page_no')

        if not pages.exists():
            return JsonResponse({'answer': 'No pages found for the given document.'}, status=404)

        # Compute similarity between the query and each page's embedding
        most_similar_page = None
        highest_similarity = -1

        for page in pages:
            page_embedding = page.vector  # Retrieve stored embedding directly
            page_similarity = compute_similarity(query_embedding, page_embedding)

            if page_similarity > highest_similarity:
                highest_similarity = page_similarity
                most_similar_page = page

        if not most_similar_page:
            return JsonResponse({'answer': 'No relevant pages found.'})

        # Set up Gmini API key
        gmini.configure(api_key="AIzaSyBiryW1HkxS-m8hyxMNbqpR-EsOMlVtIUg")

        # Generate a response using Gmini for the most similar page
        response = gmini.chat(
            prompt=(
                f"Based on the following text from page {most_similar_page.page_no}: {most_similar_page.text}\n\n"
                f"Answer the user's question: {question}. If relevant text exists across multiple pages, "
                f"mention additional pages. If no similarity is found, mention this explicitly."
            ),
            model="gpt-3.5-turbo",  # Specify the Gmini model if necessary
            max_tokens=150
        )

        # Extract the response text from Gmini
        answer = response['candidates'][0]['text']

        return JsonResponse({'page': most_similar_page.page_no, 'answer': answer})