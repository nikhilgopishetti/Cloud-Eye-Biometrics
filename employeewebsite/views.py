from django.shortcuts import render, get_object_or_404, redirect
from .models import Department, Role, Employee
from .forms import EmployeeForm
from .forms import RoleForm, DepartmentForm
from .models import Role, Department

# View for adding a role
def role_add(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleForm()
    return render(request, 'employeewebsite/role_add.html', {'form': form})

# View for adding a department
def department_add(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'employeewebsite/department_add.html', {'form': form})


def department_list(request):
    departments = Department.objects.all()
    return render(request, 'employeewebsite/department_list.html', {'departments': departments})

def department_detail(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    return render(request, 'employeewebsite/department_detail.html', {'department': department})

def role_list(request):
    roles = Role.objects.all()
    return render(request, 'employeewebsite/role_list.html', {'roles': roles})

def role_detail(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    return render(request, 'employeewebsite/role_detail.html', {'role': role})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employeewebsite/employee_list.html', {'employees': employees})

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'employeewebsite/employee_detail.html', {'employee': employee})

def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employeewebsite/employee_add.html', {'form': form})

def employee_update(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employeewebsite/employee_update.html', {'form': form})

def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employeewebsite/employee_delete.html', {'employee': employee})


def home(request):
    return render(request, 'employeewebsite/home.html')