from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseForbidden, HttpResponse
from .models import AttendanceRecord
from users import models
from datetime import timedelta, datetime
from django.template.loader import get_template
from openpyxl import Workbook
from xhtml2pdf import pisa

# from django.template.loader import render_to_string
# from django.http import HttpResponse
# from weasyprint import HTML
# from .models import AttendanceRecord
# import datetime

# def export_pdf(request):
#     logs = AttendanceRecord.objects.filter(scanned_at__date=datetime.date.today())

#     html_string = render_to_string("pdf.html", {"logs": logs})
#     html = HTML(string=html_string)

#     pdf_file = html.write_pdf()

#     response = HttpResponse(pdf_file, content_type="application/pdf")
#     response['Content-Disposition'] = 'attachment; filename="attendance_logs.pdf"'
#     return response




# ✅ Excel Export View
# def export_excel(request):
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Attendance Logs"

#     ws.append(["Name", "Status", "Time"])

#     logs = AttendanceRecord.objects.filter(timestamp__date=datetime.date.today())
#     for log in logs:
#         ws.append([log.name, log.status, log.timestamp.strftime("%I:%M %p")])

#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=attendance_logs.xlsx'
#     wb.save(response)
#     return response

 #✅ PDF Export View
def export_pdf(request):
     today = datetime.today()
     logs = AttendanceRecord.objects.filter(scanned_at__date=today)
     context = {
         "logs": logs
     }
     template = get_template("attendance/pdf.html")
     html = template.render(context)
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'attachment; filename="attendance_logs.pdf"'
     pisa.CreatePDF(html, dest=response)
     return response




@login_required
def post_login_redirect(request):
    if request.user.user_type == "teacher":
        return redirect("check_in")
    elif request.user.user_type == "secretary":
        return redirect("daily_logs")
    else:
        return redirect("admin:index")
    





@login_required
def check_in_view(request):
    user = request.user
    now = timezone.localtime()
    today = now.date()

    try:
        record = AttendanceRecord.objects.get(user=user, date=today)
        time_elapsed = (now - record.scanned_at).total_seconds()

        if record.checked_out_at:
            return redirect("scan_already_checked_out")
        elif time_elapsed >= 4 * 3600:
            record.checked_out_at = now
            record.save()
            return redirect("scan_checked_out")
        else:
            # remaining = 4 * 3600 - time_elapsed
            return redirect("scan_wait_for_checkout")
    except AttendanceRecord.DoesNotExist:
        AttendanceRecord.objects.create(user=user, scanned_at=now, date=today)
        return redirect( "scan_checked_in")




@login_required
def check_in(request):
    return render(request, "attendance/check_in.html")

@login_required
def checked_in_page(request):
    return render(request, "attendance/scan_checked_in.html")

@login_required
def checked_out_page(request):
    return render(request,"attendance/scan_checked_out.html")

@login_required
def wait_for_checkout_page(request):
    return render(request, "attendance/scan_wait_for_checkout.html")

@login_required
def already_checked_out_page(request):
    return render(request, "attendance/scan_already_checked_out.html")


@login_required
def daily_logs(request):
    if request.user.user_type.lower() != "secretary":
        return HttpResponseForbidden("Access denied.")
    else: 

        today = timezone.localdate()
        records = AttendanceRecord.objects.filter(date=today).select_related('user')


        return render(request, "attendance/daily_logs.html", {
            "records": records,
            "today": today.strftime("%A, %d %B %Y"),
            }) 
        # date_str = request.GET.get("date")
        # records = AttendanceRecord.objects.all().order_by("scanned_at")

        # if date_str:
        #     try:
        #         filter_date = timezone.datetime.strptime(date_str,"%Y-%m-%d").date()
        #         records = records.filter(scanned_at__date=filter_date)
        #     except ValueError:
        #         pass
        # return render(request,"attendance/daily_logs.html",{"records": records, "scanned_date": date_str})
    
@login_required
def teacher_home_view(request):
    return render(request, "attendance/teacher_home.html")

def download_qr_page(request):
    qr_path = "/media/qrcodes/general_qrcode.png"
    return render(request, "attendance/qrcode_download.html", {"qr_path":qr_path})






















# from django.shortcuts import render
# from django.views.generic import TemplateView
# from django.http import JsonResponse
# from .models import AttendanceLog, Classroom
# from geopy.distance import geodesic

















































































# # ======== LOOK AT THE ZEDATES FOLDER FOR ANY INFORMATION =========

# # class ScanView(TemplateView):
# #     template_name = "attendance/scan.html"

# # def log_attendance(request):
# #     if request.method == 'POST':
# #         data = request.POST
# #         try:
# #             # Validate classroom location if applicable
# #             if data.get('classroom_id'):
# #                 classroom = Classroom.objects.get(id=data['classroom_id'])
# #                 user_coords = (float(data['latitude']), float(data['longitude']))
# #                 class_coords = (classroom.latitude, classroom.longitude)
                
# #                 if geodesic(user_coords, class_coords).meters > 50:
# #                     return JsonResponse(
# #                         {"status": "error", "message": "You're too far from the classroom"},
# #                         status=400
# #                     )

# #             # Create attendance record
# #             AttendanceLog.objects.create(
# #                 user=request.user,
# #                 log_type=data['log_type'],
# #                 classroom_id=data.get('classroom_id'),
# #                 latitude=data.get('latitude'),
# #                 longitude=data.get('longitude'),
# #                 is_offline=not request.user.is_authenticated
# #             )
            
# #             return JsonResponse({"status": "success"})
            
# #         except Exception as e:
# #             return JsonResponse(
# #                 {"status": "error", "message": str(e)},
# #                 status=400
# #             )



