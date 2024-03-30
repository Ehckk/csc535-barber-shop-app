from flask import render_template, request
from .. import barber  
from ..forms.scheduleForm import BarberScheduleForm  

@barber.route("/schedule", methods=["GET", "POST"])
def schedule():
    form = BarberScheduleForm()
    if form.validate_on_submit():
        
        pass  
    return render_template("barber/schedule.html", form=form)