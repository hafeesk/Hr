from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import flt,cint, cstr, getdate
from erpnext.hr.doctype.leave_allocation.leave_allocation import get_carry_forwarded_leaves
import datetime
import dateutil.relativedelta

@frappe.whitelist()
def allocate_annual_leave_monthly():
	grat_set = frappe.db.get_value("HR Settings", None, "enable_monthly_leave_allocation")	
	frappe.msgprint("hi in annual leave")
        employee = frappe.db.sql("""select name,employee_name,vacation_starts_from from `tabEmployee` where status = 'Active'""")
        for emp in employee:
                leave_allocation_data = frappe.db.sql("""select from_date,total_leaves_allocated,name from `tabLeave Allocation` where employee = '{}' and leave_type = 'Annual Leave'""".format(emp[0]))
                frappe.msgprint(frappe.as_json(leave_allocation_data))
                if leave_allocation_data:
                        frappe.msgprint(frappe.as_json(leave_allocation_data))
                        #frappe.msgprint(frappe.as_json(max_to_date[0][0]))
			frappe.msgprint("leave allocation data")
                        if leave_allocation_data[0][0]:
                                start_date = emp[2]
                                total_leave_days = leave_allocation_data[0][1] + 2.5
                                end_date = frappe.utils.add_days(start_date,total_leave_days)
                                frappe.msgprint(frappe.as_json(start_date))
                                frappe.msgprint(frappe.as_json(end_date))
                                frappe.msgprint(frappe.as_json(total_leave_days))
                                doc = frappe.get_doc("Leave Allocation",leave_allocation_data[0][2])
                                doc.to_date = end_date
                                doc.new_leaves_allocated = total_leave_days
                                doc.total_leaves_allocated = total_leave_days
                                doc.save()
		else:
			frappe.msgprint("without leave allocation data")
                	leave_allocation_doc = frappe.new_doc("Leave Allocation")
                	leave_allocation_doc.update({'employee': emp[0], 'employee_name': emp[1],'leave_type':'Annual Leave','from_date':start_date,'to_date':end_date,'new_leaves_allocated':2.5,'carry_forward':0,'carry_forwarded_leaves':0,'total_leaves_allocated':2.5})
                	
                	leave_allocation_doc.flags.ignore_validate = True
                	leave_allocation_doc.flags.ignore_mandatory = True
                	leave_allocation_doc.flags.ignore_validate_update_after_submit = True
                	leave_allocation_doc.flags.ignore_links = True
                	leave_allocation_doc.save()
                	

        

def get_emp_gross_salary(emp):
    grat_set = frappe.db.get_value("HR Settings", None, "gratuity_base_on")
    frappe.msgprint(grat_set)
    if grat_set == "Base Salary":
    	sql = """SELECT base FROM `tabSalary Structure` ss,`tabSalary Structure Employee` se WHERE	ss.`name` = se.parent 
and se.employee = '{0}' ORDER BY se.from_date DESC LIMIT 1""".format(emp)
    else:
	sql = """SELECT (base+variable) as salary FROM `tabSalary Structure` ss,`tabSalary Structure Employee` se WHERE      ss.`name` = se.parent
and se.employee = '{0}' ORDER BY se.from_date DESC LIMIT 1""".format(emp)

    gross_salary = frappe.db.sql(sql)
    #frappe.msgprint(gross_salary)
    if gross_salary:
        gross_salary = gross_salary[0][0]
    else:
        gross_salary = 0

    return gross_salary


def get_paid_gratuity(emp, till_date):

    sql = """ select ifnull(sum(gratuity_paid),0)
		from `tabGratuity Payment`
		where employee = '{0}'
		and docstatus = 1
		and date <= '{1}' """ .format(emp, till_date)

    gratuity_paid = frappe.db.sql(sql)

    if gratuity_paid:
        gratuity_paid = gratuity_paid[0][0]
    else:
        gratuity_paid = 0

    return gratuity_paid

def calc_gratuity(no_of_years, days_per_year, gratuity_days, gross_salary):

    total_no_of_months = no_of_years * 12
    # total_no_of_months = 168
     
    total_no_of_days_gratuity = no_of_years * days_per_year
    # total_no_of_days_gratuity = 4936

    total_no_of_days_for_gratuity = no_of_years * gratuity_days
    # total_no_of_days_for_gratuity =====> 11 years = 330, 3 years = 45 ===> 375

    days_per_month_gratuity = total_no_of_days_for_gratuity / total_no_of_months
    # days_per_month_gratuity = 2.2321425

    gratuity_per_working_day = days_per_month_gratuity / 30
    #  gratuity_per_working_day = 0.07440475

    gratuity_for_total_working_days = gratuity_per_working_day * total_no_of_days_gratuity
    # gratuity_for_total_working_days = 367.261846

    basic_salary = gross_salary * 12
    # basic_salary = 5400

    per_day_basic_salary = basic_salary / 365
    # per_day_basic_salary = 14.79

    amount_of_gratuity = (per_day_basic_salary * gratuity_for_total_working_days) or 0
    # amount_of_gratuity = 5431.8027
    return amount_of_gratuity


def get_gratuity_calc_start_date(emp):

    sql = """SELECT ifnull(max(p.date), e.date_of_joining) dated
	FROM `tabGratuity Payment` p
	RIGHT OUTER JOIN tabEmployee e on (p.employee = e.`name`)
	WHERE e.`name` = '{0}' """.format(emp)

    d = frappe.db.sql(sql)
    if d:
        d = d[0][0]

    return d

@frappe.whitelist()
def calculate_gratuity():
	
    
	sql = """ Select name, employee_name, gratuity_payable_till_date, gratuity_till_date, date_of_joining,country from `tabEmployee`
        	where `status`= 'Active' """

        emp_list = frappe.db.sql(sql, as_dict=1)
	days_per_year = 365.0
        now = datetime.datetime.now().date()
	cur_year = datetime.datetime.now().year
	s_now = now.strftime('%Y-%m-%d')
	
        for emp in emp_list:
	    if emp.country == "Bahrain":
		continue

            joining_date = emp.date_of_joining
	    last_working_year = joining_date.replace(year=cur_year)
	    if(last_working_year > now):
		last_working_year = joining_date.replace(year=cur_year-1)	
            #frappe.msgprint(frappe.as_json(last_working_year))
            last_year_working_days = now-last_working_year
            #frappe.msgprint(frappe.as_json(last_year_working_days.days))

            diff = dateutil.relativedelta.relativedelta(now, joining_date)
            working_years = dateutil.relativedelta.relativedelta(now, joining_date).years
	    #frappe.msgprint(str(working_years))
            gross_salary = get_emp_gross_salary(emp.name)

            sum_gross_gratuity = 0
            sum_gross_payable = 0
	    #frappe.msgprint(str(working_years))
	    count = 0
	    if working_years >=1:        
	        for yc in range(1,working_years+1):
                    if yc > 3.0:
			count = count + 1
                        gratuity_days = 30.0
                        gross_gratuity = calc_gratuity(1, days_per_year, gratuity_days, gross_salary)
			frappe.msgprint(str(gross_gratuity))
                        sum_gross_gratuity += gross_gratuity
#			#frappe.msgprint(str(sum_gross_gratuity))
                    else:
			if yc >= 1:
			    count = count + 1
                            gratuity_days = 15.0
                            gross_gratuity = calc_gratuity(1, days_per_year, gratuity_days, gross_salary)
			    frappe.msgprint(str(gross_gratuity))
                            sum_gross_gratuity += gross_gratuity
#			    #frappe.msgprint(str(sum_gross_gratuity))
		frappe.msgprint(str(count))
	    else:
		sum_gross_gratuity = 0
	    if last_year_working_days.days:
		
		frappe.msgprint(str(last_year_working_days.days))
		year_per = last_year_working_days.days/365.00
		frappe.msgprint(str(year_per))
		if working_years >= 1 and working_years <3:
			gross_gratuity = (gross_salary/2) * year_per
		elif working_years >= 3:
			gross_gratuity = gross_salary * year_per
		else:
			gross_gratuity = (gross_salary/2) * year_per
		frappe.msgprint(str(gross_gratuity))
		sum_gross_gratuity += gross_gratuity

	    #frappe.msgprint(emp.name)
            emp_doc = frappe.get_doc('Employee', emp.name)
            emp_doc.gratuity_till_date = sum_gross_gratuity
            emp_doc.gratuity_payable_till_date = sum_gross_gratuity - emp_doc.gratuity_paid_till_date
            
            emp_doc.save()

            #frappe.db.commit()
     	    
	

