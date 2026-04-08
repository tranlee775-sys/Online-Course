from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment
import logging

# Thiết lập logger để theo dõi lỗi nếu cần
logger = logging.getLogger(__name__)

# Class-based view cho danh sách khóa học
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')[:10]

# Class-based view cho chi tiết khóa học
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

# Hàm xử lý đăng ký (nếu bạn cần dùng)
def registration(request):
    # Logic đăng ký tài khoản có thể thêm ở đây
    pass

# Hàm xử lý đăng nhập
def login_request(request):
    # Logic đăng nhập tài khoản có thể thêm ở đây
    pass

# Hàm xử lý đăng xuất
def logout_request(request):
    logout(request)
    return HttpResponseRedirect(reverse('onlinecourse:index'))

# --------------------------------------------------------------------------
# TASK 5: Hàm submit để xử lý dữ liệu từ Form bài thi
# --------------------------------------------------------------------------
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # 1. Lấy tất cả choice_id mà người dùng đã tick từ POST request
        # Các checkbox trong HTML có name="choice_{{choice.id}}"
        selected_ids = [int(value) for key, value in request.POST.items() if 'choice_' in key]
        
        # 2. Tìm bản ghi Enrollment của User hiện tại cho khóa học này
        enrollment = Enrollment.objects.get(user=request.user, course=course)
        
        # 3. Tạo một bản ghi Submission mới gắn với Enrollment đó
        submission = Submission.objects.create(enrollment=enrollment)
        
        # 4. Lưu các lựa chọn người dùng đã chọn vào ManyToMany field 'choices' của Submission
        for choice_id in selected_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
            
        # 5. Chuyển hướng sang trang kết quả bài thi
        return redirect('onlinecourse:show_exam_result', submission.id)

# --------------------------------------------------------------------------
# TASK 5: Hàm hiển thị kết quả và tính toán điểm số
# --------------------------------------------------------------------------
def show_exam_result(request, submission_id):
    # 1. Truy vấn thông tin Submission và Course liên quan
    submission = get_object_or_404(Submission, pk=submission_id)
    course = submission.enrollment.course
    
    # 2. Khởi tạo biến để tính toán
    total_score = 0
    results = []
    
    # 3. Duyệt qua từng bài học và từng câu hỏi trong khóa học
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            # Lấy danh sách ID các lựa chọn mà User đã nộp cho câu hỏi này
            selected_ids = submission.choices.filter(question=question).values_list('id', flat=True)
            
            # Gọi phương thức is_get_score đã định nghĩa ở Task 1 trong models.py
            is_correct = question.is_get_score(selected_ids)
            
            # Nếu trả lời đúng, cộng dồn điểm của câu hỏi đó
            if is_correct:
                total_score += question.grade
            
            # Lưu kết quả chi tiết để hiển thị lên template
            results.append({
                'question': question,
                'is_correct': is_correct,
                'selected_ids': list(selected_ids)
            })

    # 4. Đưa dữ liệu vào Context để render ra template kết quả
    context = {
        'submission': submission,
        'course': course,
        'total_score': total_score,
        'results': results
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)