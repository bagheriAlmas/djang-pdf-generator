from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Note


class NoteListView(ListView):
    model = Note
    template_name = 'home.html'
    context_object_name = 'notes'


class NoteDetailView(DetailView):
    model = Note
    template_name = 'notes/note.html'
    context_object_name = 'note'


class NoteCreateView(CreateView):
    model = Note
    template_name = 'notes/create_note.html'
    fields = ['title', 'body', 'thumbnail']
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(UpdateView):
    model = Note
    template_name = 'notes/update_note.html'
    fields = ['title', 'body', 'thumbnail']
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'notes/delete_note.html'
    success_url = reverse_lazy('note_list')
