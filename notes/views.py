from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template.loader import get_template
from django.shortcuts import render
from django.conf import settings
import os.path
from xhtml2pdf import pisa
from datetime import datetime
from .models import Note, Report


class PDFRenderView(ListView):
    model = Note
    template_name = 'reports/pdf_template.html'
    context_object_name = 'notes'

    def render_to_response(self, context, **response_kwargs):

        template = get_template(self.template_name)
        html = template.render(context)

        user = self.request.user
        if user.is_authenticated:
            username = user.username
        else:
            username = 'anonymous'

        file_directory = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(file_directory, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f'report_{username}_{timestamp}.pdf'
        pdf_file_path = os.path.join(file_directory, pdf_filename)

        with open(pdf_file_path, 'wb') as pdf_file:
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)
            if pisa_status.err:
                return render(self.request, 'reports/pdf_message.html', {'message': 'PDF creation error'})

        pdf_url = os.path.join(settings.MEDIA_URL, 'reports', pdf_filename)

        Report.objects.create(
            author=user,
            file=pdf_url
        )
        return render(self.request, 'reports/pdf_message.html', {'message': 'Your request is being processed'})


class PDFReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/pdf_report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.filter(author=self.request.user)


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'home.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note.html'
    context_object_name = 'note'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'notes/create_note.html'
    fields = ['title', 'body', 'thumbnail']
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    template_name = 'notes/update_note.html'
    fields = ['title', 'body', 'thumbnail']
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.author = self.request.user

        instance = form.save(commit=False)
        uploaded_image = form.cleaned_data['thumbnail']
        instance.thumbnail = uploaded_image
        instance.save()

        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = 'notes/delete_note.html'
    success_url = reverse_lazy('note_list')

    def test_func(self):
        return self.get_object().author == self.request.user
