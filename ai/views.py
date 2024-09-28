# my_app/views.py
import os
import openai
from django.http import JsonResponse
from django.views import View
from .models import PDFPage, PDFDocument
from .embedding_service import generate_embedding, compute_similarity
import fitz  # PyMuPDF

class PDFUploadView(View):
    def post(self, request):
        file = request.FILES['pdf_file']
        pdf_document = PDFDocument.objects.create(file=file)
        
        
        # Dictionary to store embeddings for all pages
        embeddings_dict = {}

        with fitz.open(file) as pdf:
            for page_num in range(len(pdf)):
                page = pdf.load_page(page_num)
                text = page.get_text("text")

                # Generate embedding for the page text
                embedding = generate_embedding(text)
                
                # Store the page text in the embeddings dictionary
                embeddings_dict[str(page_num + 1)] = text

                # Store the page text and its embedding in the database
                PDFPage.objects.create(
                    document=pdf_document,
                    page_number=page_num + 1,
                    text=text,
                    embedding=embedding # Store as dictionary
                )

        return JsonResponse({'message': 'PDF uploaded and processed successfully'})

class PDFQueryView(View):
    def post(self, request, document_id):
        question = request.POST.get('question')

        # Generate embedding for the user's query
        query_embedding = generate_embedding(question)

        # Retrieve all the pages from the specified document
        pages = PDFPage.objects.filter(document_id=document_id)

        if not pages.exists():
            return JsonResponse({'answer': 'No pages found for the given document.'})

        # Compute similarity between the query and each page's embedding
        most_similar_page = None
        highest_similarity = -1

        for page in pages:
            # Get the embedding from the dictionary
            page_embedding = generate_embedding(page.text)  # Generate embedding for the page text
            page_similarity = compute_similarity(query_embedding, page_embedding)

            if page_similarity > highest_similarity:
                highest_similarity = page_similarity
                most_similar_page = page

        if not most_similar_page:
            return JsonResponse({'answer': 'No relevant pages found.'})

        # Use OpenAI to generate a response based on the most similar page text
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Based on the following text from page {most_similar_page.page_number}: {most_similar_page.text}\n\nAnswer the user's question: {question}.And if you think that the similarity text is exist more then dont provide text you should increase the page number size and if the similarity text is not exist now then provide text with page number.",
            max_tokens=150
        )
        answer = response.choices[0].text.strip()

        return JsonResponse({ 'page': most_similar_page.page_number,'answer': answer})
