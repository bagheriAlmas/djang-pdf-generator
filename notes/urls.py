from django.urls import path
from .views import (NoteListView, NoteDetailView, NoteCreateView, NoteUpdateView, NoteDeleteView, PDFRenderView,
                    PDFReportListView)

urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('note/create/', NoteCreateView.as_view(), name='note_create'),
    path('note/<int:pk>/update/', NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
    path('pdf/request/', PDFRenderView.as_view(), name='pdf_render'),
    path('pdf/reports/', PDFReportListView.as_view(), name='pdf_report_list'),

]
