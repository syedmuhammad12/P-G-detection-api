from django.http import HttpResponse
from django.template.loader import get_template
from numpy import source
from xhtml2pdf import pisa
from quality_assurance_system.models import *

def generateEtamuReport(context_dict={}):

    output_filename = "report.pdf"
    data = Bottle.objects.all()

    template_1 = get_template("pdf/report/part_1.html")
    source_html_1  = template_1.render(context_dict)

    template_2 = get_template("pdf/report/part_2.html")
    source_html_2  = template_2.render(context_dict)

    template_3 = get_template("pdf/report/part_3.html")
    source_html_3  = template_3.render(context_dict)

    template_4 = get_template("pdf/report/part_4.html")
    source_html_4  = template_4.render(context_dict)

    template_5 = get_template("pdf/report/part_5.html")
    source_html_5  = template_5.render(context_dict)

    template_6 = get_template("pdf/report/part_6.html")
    source_html_6  = template_6.render(context_dict)

    result_file = open(output_filename, "w+b")

    rows = ""
    
    for bottle in data:

        rows += '<tr><td style="font-family:Verdana, Geneva, sans-serif; font-size:13px; padding-top: 3px;  border-top:1px solid #333; border-bottom:1px solid #333; border-left:1px solid #333; border-right:1px solid #333;" width="34%" height="32" align="center">'+ str(bottle.id) +'</td><td style="font-family:Verdana, Geneva, sans-serif; font-size:13px; padding-top: 3px;  border-top:1px solid #333; border-bottom:1px solid #333; border-right:1px solid #333;" width="26%" align="center">'+ bottle.result +'</td><td style="font-family:Verdana, Geneva, sans-serif; font-size:13px; padding-top: 3px;  border-top:1px solid #333; border-bottom:1px solid #333; border-right:1px solid #333;" width="25%" align="center" colspan="2">'+ str(bottle.created_at) +'</td></tr>'
    
    count_of_total_bottles = Bottle.objects.count()
    count_of_acceptable_bottles = Bottle.objects.filter(result="Acceptable").count()
    count_of_unacceptable_bottles = Bottle.objects.filter(result="Unacceptable").count()

    source_html = source_html_1 + "2022/03/20 - 2022/04/20" + source_html_2 + "<b># of Acceptable bottles = </b>"+ str(count_of_acceptable_bottles) + source_html_3 + "<b># of Unacceptable bottles = </b>"+ str(count_of_unacceptable_bottles) + source_html_4 + "<b>Total # of bottles = </b>"+ str(count_of_total_bottles) + source_html_5 + rows + source_html_6

    pisa_status = pisa.CreatePDF(source_html, dest=result_file)

    result_file.close()

    return pisa_status.err