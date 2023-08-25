from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Note


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
