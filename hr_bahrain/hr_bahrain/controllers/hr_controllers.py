from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import flt,cint, cstr, getdate

def allocate_annual_leave_monthly():
	frappe.msgprint('hi')
        employee = frappe.db.sql("""select name,employee_name,vacation_starts_from from `tabEmployee` where status = 'Active'""")
        for emp in employee:
                max_to_date = frappe.db.sql("""select MAX(to_date) from `tabLeave Allocation` where employee = '{}'""".format(emp[0]))

                if max_to_date:
                        #frappe.msgprint(frappe.as_json(max_to_date))
                        #frappe.msgprint(frappe.as_json(max_to_date[0][0]))

                        if not max_to_date[0][0]:
                                start_date = emp[2]
                                end_date = frappe.utils.add_days(start_date,2)
                                #frappe.msgprint('1')
                                #frappe.msgprint(frappe.as_json(start_date))
                                #frappe.msgprint(frappe.as_json(end_date))

                        else:
                                start_date = max_to_date[0][0]
                                end_date = frappe.utils.add_days(start_date,2)
                                #frappe.msgprint('2')
                                #frappe.msgprint(frappe.as_json(start_date))
                                #frappe.msgprint(frappe.as_json(end_date))
                carry_fwd_leave = get_carry_forwarded_leaves(emp[0],'Casual Leave',start_date,1)
                if carry_fwd_leave % 1 == 0:
                        end_date = frappe.utils.add_days(end_date,1)
                #frappe.msgprint('hi')
                #frappe.msgprint(frappe.as_json(carry_fwd_leave))
                leave_allocation_doc = frappe.new_doc("Leave Allocation")
                leave_allocation_doc.update({'employee': emp[0], 'employee_name': emp[1],'leave_type':'Casual Leave','from_date':start_date,'to_date':end_date,'new_leaves_allocated':2.5,'carry_forward':1,'carry_forwarded_leaves':carry_fwd_leave,'total_leaves_allocated':carry_fwd_leave+2.5})
                leave_allocation_doc.docstatus = 1
                leave_allocation_doc.flags.ignore_validate = True
                leave_allocation_doc.flags.ignore_mandatory = True
                leave_allocation_doc.flags.ignore_validate_update_after_submit = True
                leave_allocation_doc.flags.ignore_links = True
                leave_allocation_doc.save()
                leave_allocation_doc.submit()

        frappe.db.commit()

