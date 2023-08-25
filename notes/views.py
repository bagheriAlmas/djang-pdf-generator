from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Note


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'home.html'
    context_object_name = 'notes'


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note.html'
    context_object_name = 'note'


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'notes/create_note.html'
    fields = ['title', 'body', 'thumbnail']
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
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


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/delete_note.html'
    success_url = reverse_lazy('note_list')
