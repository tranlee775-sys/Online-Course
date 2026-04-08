from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Route cho danh sách khóa học (trang chủ của app)
    path(route='', view=views.CourseListView.as_view(), name='index'),
    
    # Route cho đăng ký và đăng nhập
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    # Route cho chi tiết khóa học: /onlinecourse/5/
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),

    # ----------------------------------------------------------------------
    # TASK 6: THÊM CÁC PATH CHO SUBMIT VÀ SHOW_EXAM_RESULT
    # ----------------------------------------------------------------------
    
    # Path để xử lý nộp bài thi
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    
    # Path để hiển thị kết quả sau khi nộp
    path('submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),

] + static(settings.MEDIA_URL, document_root=settings.DOCUMENT_ROOT)