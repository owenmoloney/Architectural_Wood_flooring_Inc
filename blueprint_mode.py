"""
Owen Moloney 
Blueprint Visual Reference Mode
Enhanced version with blueprint image display for guided manual entry
Uses the same calculation engine from main.py
"""

from main import FlooringJob, Room, Obstacle, Employee, print_cost_report
import os
import io


def display_blueprint(blueprint_path: str = None):
    """Display blueprint image or PDF to user"""
    if not blueprint_path or not os.path.exists(blueprint_path):
        print("\nNo blueprint file found.")
        print("You can continue without a blueprint.")
        choice = input("Continue without blueprint? (yes/no): ").strip().lower()
        return choice in ['yes', 'y']
    
    # Check if it's a PDF
    is_pdf = blueprint_path.lower().endswith('.pdf')
    
    try:
        print("\n" + "="*60)
        print("         BLUEPRINT REFERENCE")
        print("="*60)
        print(f"\nLoading blueprint: {blueprint_path}")
        
        if is_pdf:
            # Handle PDF files
            try:
                import fitz  # PyMuPDF
                print("   File type: PDF")
                
                # Open PDF and get first page
                pdf_doc = fitz.open(blueprint_path)
                first_page = pdf_doc[0]
                
                # Convert to image
                zoom = 2.0  # Increase resolution
                mat = fitz.Matrix(zoom, zoom)
                pix = first_page.get_pixmap(matrix=mat)
                
                print(f"   Pages: {len(pdf_doc)}")
                
                # Convert to PIL Image
                from PIL import Image
                img_data = pix.tobytes("ppm")
                img = Image.open(io.BytesIO(img_data))
                width, height = img.size
                print(f"   Display size: {width} × {height} pixels")
                
                pdf_doc.close()
                
            except ImportError:
                print("\nPyMuPDF not installed for PDF support.")
                print("Install with: pip install pymupdf")
                print("   Trying to open PDF with system default viewer...")
                
                # Try to open with system default
                import subprocess
                import platform
                if platform.system() == 'Darwin':  # macOS
                    subprocess.call(['open', blueprint_path])
                elif platform.system() == 'Windows':
                    os.startfile(blueprint_path)
                else:  # Linux
                    subprocess.call(['xdg-open', blueprint_path])
                
                print("\nPDF opened in system viewer.")
                input("   Press Enter when ready to start entering measurements...")
                return True
            except Exception as e:
                print(f"\nCould not process PDF: {e}")
                choice = input("Continue anyway? (yes/no): ").strip().lower()
                return choice in ['yes', 'y']
        else:
            # Handle regular image files
            from PIL import Image
            img = Image.open(blueprint_path)
            width, height = img.size
            print(f"   File type: Image")
            print(f"   Size: {width} × {height} pixels")
        
        # Show the image
        print("\nKeep blueprint visible while entering measurements.")
        
        img.show()
        print("\nBlueprint opened in image viewer.")
        input("   Press Enter when ready to start entering measurements...")
        return True
        
    except ImportError:
        print("\nPIL/Pillow not installed. Install with: pip install pillow")
        print("   Continuing without image display...")
        return True
    except Exception as e:
        print(f"\nCould not open blueprint: {e}")
        choice = input("Continue anyway? (yes/no): ").strip().lower()
        return choice in ['yes', 'y']


def get_room_input_with_reference(room_number: int) -> Room:
    """Get room information with visual reference"""
    print(f"\n{'─'*60}")
    print(f"ROOM #{room_number} - Refer to your blueprint for dimensions")
    print(f"{'─'*60}")
    
    room_name = input("Room name: ").strip()
    if not room_name:
        print("Please enter a room name.")
        return None
    
    # Give user choice: L×W or direct area
    print("\nHow would you like to enter the room size?")
    print("  1. Length × Width (I'll calculate area)")
    print("  2. Total square feet (direct)")
    
    while True:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == '1':
            # Length × Width method
            try:
                length = float(input(f"Length of {room_name} (ft): "))
                width = float(input(f"Width of {room_name} (ft): "))
                total_area = length * width
                print(f"Calculated area: {total_area:.2f} sq ft")
                break
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue
        
        elif choice == '2':
            # Direct square feet
            try:
                total_area = float(input(f"Total area of {room_name} (sq ft): "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
        
        else:
            print("Please enter 1 or 2.")
    
    room = Room(room_name, total_area)
    
    # Add obstacles
    print(f"\nAdd obstacles for {room_name}:")
    print("(Enter 'none' to skip)")
    
    obstacle_count = 0
    while True:
        obstacle_name = input(f"Obstacle #{obstacle_count + 1} name (or 'none'): ").strip()
        if obstacle_name.lower() == 'none' or not obstacle_name:
            break
        
        try:
            obstacle_area = float(input(f"  Area of {obstacle_name} (sq ft): "))
            room.obstacles.append(Obstacle(obstacle_name, obstacle_area))
            obstacle_count += 1
            print(f"  Added {obstacle_name}: {obstacle_area} sq ft")
        except ValueError:
            print("  Invalid input. Please enter a number.")
    
    usable = room.get_usable_area()
    print(f"\n{room_name}: {total_area:.2f} sq ft total, {usable:.2f} sq ft usable")
    
    return room


def get_employee_input_with_reference() -> list:
    """Get employee information with clear prompts"""
    employees = []
    
    print("\n" + "="*60)
    print("EMPLOYEE INFORMATION")
    print("="*60)
    print("Enter each person who will work on this job.")
    
    while True:
        name = input("\nEmployee name (or 'done'): ").strip()
        if name.lower() == 'done':
            break
        if not name:
            continue
        
        try:
            rate = float(input(f"  Hourly rate for {name} ($): "))
            employees.append(Employee(name, rate))
            print(f"  Added {name}: ${rate:.2f}/hour")
        except ValueError:
            print("  Invalid input. Please enter a number.")
    
    return employees


def get_job_parameters_with_reference() -> dict:
    """Get job parameters with guided input"""
    params = {}
    
    print("\n" + "="*60)
    print("JOB PARAMETERS")
    print("="*60)
    
    # Days
    print("\nWork Schedule:")
    while True:
        try:
            params['days'] = int(input("How many 8-hour days? "))
            if params['days'] > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")
    
    # Sanding cost per sq ft
    print("\nSanding Cost:")
    while True:
        try:
            params['sanding'] = float(input("Sanding cost per sq ft ($): "))
            if params['sanding'] >= 0:
                break
            print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Material info
    print("\nMaterial Information:")
    while True:
        provides = input("Will customer provide wood? (yes/no): ").strip().lower()
        if provides in ['yes', 'y']:
            params['customer_provides_wood'] = True
            params['material_cost'] = 0.0
            params['pickup_fee'] = 0.0
            break
        elif provides in ['no', 'n']:
            params['customer_provides_wood'] = False
            while True:
                try:
                    params['material_cost'] = float(input("Material cost per sq ft ($): "))
                    if params['material_cost'] >= 0:
                        break
                    print("Please enter a non-negative number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            while True:
                try:
                    params['pickup_fee'] = float(input("Pickup/delivery fee ($): "))
                    if params['pickup_fee'] >= 0:
                        break
                    print("Please enter a non-negative number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            break
        else:
            print("Please enter 'yes' or 'no'.")
    
    return params


def review_before_calculate(job: FlooringJob) -> bool:
    """Show review screen and get confirmation"""
    print("\n" + "="*60)
    print("         REVIEW BEFORE CALCULATION")
    print("="*60)
    
    print(f"\nFLOORS ({len(job.rooms)} rooms):")
    for i, room in enumerate(job.rooms, 1):
        obstacles = f"{len(room.obstacles)} obstacles" if room.obstacles else "no obstacles"
        print(f"   {i}. {room.name}: {room.get_usable_area():.2f} sq ft ({obstacles})")
    
    print(f"\nEMPLOYEES ({len(job.employees)}):")
    for emp in job.employees:
        print(f"   {emp.name}: ${emp.hourly_rate:.2f}/hour")
    
    print(f"\nSCHEDULE:")
    print(f"   {job.days_required} days × 8 hours = {job.days_required * 8} total hours")
    
    print(f"\nCOSTS:")
    print(f"   Sanding: ${job.sanding_cost_per_sqft:.2f}/sq ft")
    if not job.customer_provides_wood:
        print(f"   Material: ${job.material_cost_per_sqft:.2f}/sq ft")
        print(f"   Pickup Fee: ${job.pickup_fee:.2f}")
    else:
        print(f"   Material: Customer provides")
    
    print(f"\n{'─'*60}")
    
    while True:
        confirm = input("\nDoes this look correct? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            return True
        elif confirm in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")


def create_job_from_blueprint_reference(blueprint_path: str = None) -> FlooringJob:
    """Create job with blueprint visual reference"""
    # Try to display blueprint
    display_blueprint(blueprint_path)
    
    print("\n" + "="*60)
    print("   BLUEPRINT VISUAL REFERENCE MODE")
    print("="*60)
    print("Entering Room Information")
    print("View blueprint as you enter measurements.")
    
    # Get rooms
    rooms = []
    room_num = 1
    
    while True:
        room = get_room_input_with_reference(room_num)
        if not room:
            print("Skipping this room...")
            continue
        
        rooms.append(room)
        room_num += 1
        
        more = input("\nAdd another room? (yes/no): ").strip().lower()
        if more not in ['yes', 'y']:
            break
    
    if not rooms:
        print("\nNo rooms added.")
        return None
    
    # Get employees
    employees = get_employee_input_with_reference()
    if not employees:
        print("\nNo employees added.")
        return None
    
    # Get job parameters
    params = get_job_parameters_with_reference()
    
    # Create job
    job = FlooringJob()
    job.rooms = rooms
    job.employees = employees
    job.days_required = params['days']
    job.sanding_cost_per_sqft = params['sanding']
    job.customer_provides_wood = params['customer_provides_wood']
    job.material_cost_per_sqft = params.get('material_cost', 0.0)
    job.pickup_fee = params.get('pickup_fee', 0.0)
    
    # Review and confirm
    if not review_before_calculate(job):
        print("\nCalculation cancelled.")
        return None
    
    return job


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  BLUEPRINT VISUAL REFERENCE CALCULATOR")
    print("="*60)
    print("\nEnter measurements while viewing blueprint for reference.")
    
    # Ask if they have a blueprint
    print("\nDo you have a blueprint file to reference?")
    has_blueprint = input("Enter file path (or press Enter to skip): ").strip()
    
    blueprint_path = has_blueprint if has_blueprint else None
    
    # Create job
    job = create_job_from_blueprint_reference(blueprint_path)
    
    if job:
        # Show results
        print_cost_report(job)
        
        # Ask if another job
        while True:
            again = input("\nCalculate another job? (yes/no): ").strip().lower()
            if again in ['yes', 'y']:
                job = create_job_from_blueprint_reference(blueprint_path)
                if job:
                    print_cost_report(job)
            elif again in ['no', 'n']:
                print("\nThank you.")
                break
            else:
                print("Please enter 'yes' or 'no'.")
    else:
        print("\nJob creation cancelled.")

