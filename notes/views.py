from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from pdf_generator import settings
from .forms import EventForm
from .models import Note, Report
from .tasks import generate_report_data_for_user
from django.shortcuts import render


class PDFRenderView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/pdf_select_report_period.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventForm()
        context['message'] = 'Your request is being processed'
        return context

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            generate_report_data_for_user(request.user.id, start_date, end_date)
            return render(request, 'reports/pdf_message.html', {})
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class PDFReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/pdf_report_list.html'
    context_object_name = 'reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CDN_DOWNLOAD_URL'] = settings.CDN_DOWNLOAD_URL
        return context

    def get_queryset(self):
        return Report.objects.filter(author=self.request.user)


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'home.html'
    context_object_name = 'notes'
    paginate_by = 6

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = context.get('page_obj')
        return context


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
