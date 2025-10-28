"""
Owen Moloney 
Wood Flooring Calculator
Calculates total cost for hardwood floor installation including:
- Material costs
- Labor costs (multiple employees)
- Sanding costs
- Obstacle exclusions (fireplaces, closets, etc.)
- Pickup fees
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Obstacle:
    """Represents obstacles in a room (fireplaces, closets, etc.)"""
    name: str
    area_sqft: float


@dataclass
class Room:
    """Represents a room with measurements and obstacles"""
    name: str
    total_area_sqft: float
    obstacles: List[Obstacle] = field(default_factory=list)
    
    def get_usable_area(self) -> float:
        """Calculate usable floor space excluding obstacles"""
        obstacle_area = sum(obs.area_sqft for obs in self.obstacles)
        return self.total_area_sqft - obstacle_area


@dataclass
class Employee:
    """Represents an employee with their hourly rate"""
    name: str
    hourly_rate: float


@dataclass
class FlooringJob:
    """Complete flooring job with all cost components"""
    rooms: List[Room] = field(default_factory=list)
    employees: List[Employee] = field(default_factory=list)
    days_required: int = 0
    
    # Costs
    sanding_cost_per_sqft: float = 0.0
    material_cost_per_sqft: float = 0.0
    customer_provides_wood: bool = True
    pickup_fee: float = 0.0
    
    def get_total_floor_space(self) -> float:
        """Calculate total usable floor space across all rooms"""
        return sum(room.get_usable_area() for room in self.rooms)
    
    def calculate_material_cost(self) -> float:
        """Calculate material cost including waste factor"""
        if self.customer_provides_wood:
            return 0.0
        
        usable_area = self.get_total_floor_space()
        # Add 10% waste factor for cutouts and mistakes
        material_needed = usable_area * 1.10
        
        material_cost = material_needed * self.material_cost_per_sqft
        
        # Add pickup fee if applicable
        if not self.customer_provides_wood:
            material_cost += self.pickup_fee
        
        return material_cost
    
    def calculate_labor_cost(self) -> float:
        """Calculate total labor cost for all employees"""
        hours_per_day = 8
        total_hours = self.days_required * hours_per_day
        
        total_labor_cost = 0.0
        for employee in self.employees:
            total_labor_cost += employee.hourly_rate * total_hours
        
        return total_labor_cost
    
    def calculate_sanding_cost(self) -> float:
        """Calculate sanding cost based on per sq ft rate"""
        usable_area = self.get_total_floor_space()
        return usable_area * self.sanding_cost_per_sqft
    
    def calculate_total_cost(self) -> float:
        """Calculate total project cost"""
        material = self.calculate_material_cost()
        labor = self.calculate_labor_cost()
        sanding = self.calculate_sanding_cost()
        
        return material + labor + sanding
    
    def get_cost_breakdown(self) -> dict:
        """Get detailed cost breakdown"""
        return {
            "total_floor_space_sqft": self.get_total_floor_space(),
            "material_cost": self.calculate_material_cost(),
            "labor_cost": self.calculate_labor_cost(),
            "sanding_cost": self.calculate_sanding_cost(),
            "total_cost": self.calculate_total_cost(),
            "customer_provides_wood": self.customer_provides_wood,
            "sanding_cost_per_sqft": self.sanding_cost_per_sqft
        }


def print_cost_report(job: FlooringJob):
    """Print a formatted cost report"""
    breakdown = job.get_cost_breakdown()
    
    print("\n" + "="*60)
    print("           FLOORING PROJECT COST ESTIMATE")
    print("="*60)
    
    print(f"\nFLOOR SPACE:")
    print(f"   Total Usable Area: {breakdown['total_floor_space_sqft']:.2f} sq ft")
    
    if job.rooms:
        print(f"\n   Room Breakdown:")
        for room in job.rooms:
            usable = room.get_usable_area()
            obstacle_area = sum(o.area_sqft for o in room.obstacles)
            print(f"   {room.name}: {usable:.2f} sq ft usable")
            if obstacle_area > 0:
                print(f"     (Excluding {obstacle_area:.2f} sq ft of obstacles)")
    
    print(f"\nCOST BREAKDOWN:")
    print(f"   Sanding Cost:        ${breakdown['sanding_cost']:,.2f}")
    print(f"     ({breakdown['total_floor_space_sqft']:.2f} sq ft × ${breakdown['sanding_cost_per_sqft']:.2f}/sq ft)")
    print(f"   Labor Cost:          ${breakdown['labor_cost']:,.2f}")
    
    if not breakdown['customer_provides_wood']:
        print(f"   Material Cost:       ${breakdown['material_cost']:,.2f}")
    else:
        print(f"   Material Cost:       $0.00 (Customer provides wood)")
    
    print(f"\n{'─'*60}")
    print(f"   TOTAL PROJECT COST:  ${breakdown['total_cost']:,.2f}")
    print("="*60 + "\n")


def get_room_input() -> List[Room]:
    """Get room and obstacle information from user"""
    rooms = []
    
    print("\n" + "="*60)
    print("ROOM INFORMATION")
    print("="*60)
    
    while True:
        room_name = input("\nEnter room name (or 'done' to finish): ").strip()
        if room_name.lower() == 'done':
            break
        if not room_name:
            print("Please enter a room name.")
            continue
        
        try:
            total_area = float(input(f"Enter total area for {room_name} (sq ft): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        room = Room(room_name, total_area)
        
        # Add obstacles
        print(f"\nAdd obstacles for {room_name} (or 'none' to skip):")
        while True:
            obstacle_name = input("Enter obstacle name (or 'none' to finish): ").strip()
            if obstacle_name.lower() == 'none':
                break
            if not obstacle_name:
                continue
            
            try:
                obstacle_area = float(input(f"Enter area for {obstacle_name} (sq ft): "))
                room.obstacles.append(Obstacle(obstacle_name, obstacle_area))
                print(f"Added {obstacle_name} ({obstacle_area} sq ft)")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        rooms.append(room)
        print(f"\nAdded {room_name}: {room.get_usable_area():.2f} sq ft usable area")
    
    return rooms


def get_employee_input() -> List[Employee]:
    """Get employee information from user"""
    employees = []
    
    print("\n" + "="*60)
    print("EMPLOYEE INFORMATION")
    print("="*60)
    
    while True:
        name = input("\nEnter employee name (or 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        if not name:
            print("Please enter a name.")
            continue
        
        try:
            hourly_rate = float(input(f"Enter hourly rate for {name} ($): "))
            employees.append(Employee(name, hourly_rate))
            print(f"Added {name}: ${hourly_rate:.2f}/hour")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return employees


def get_job_input() -> dict:
    """Get job parameters from user"""
    print("\n" + "="*60)
    print("JOB PARAMETERS")
    print("="*60)
    
    params = {}
    
    # Days required
    while True:
        try:
            params['days'] = int(input("\nHow many 8-hour days will the job take? "))
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
    
    # Sanding cost
    while True:
        try:
            params['sanding'] = float(input("Enter sanding cost per sq ft ($): "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Material information
    print("\nMaterial Information:")
    while True:
        provides = input("Will the customer provide the wood? (yes/no): ").strip().lower()
        if provides in ['yes', 'y']:
            params['customer_provides_wood'] = True
            params['material_cost'] = 0.0
            params['pickup_fee'] = 0.0
            break
        elif provides in ['no', 'n']:
            params['customer_provides_wood'] = False
            while True:
                try:
                    params['material_cost'] = float(input("Enter material cost per sq ft ($): "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
            while True:
                try:
                    params['pickup_fee'] = float(input("Enter pickup/delivery fee ($): "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
            break
        else:
            print("Please enter 'yes' or 'no'.")
    
    return params


def create_job_from_input() -> FlooringJob:
    """Create a FlooringJob from user input"""
    # Get rooms
    rooms = get_room_input()
    
    if not rooms:
        print("\nNo rooms added. Exiting.")
        return None
    
    # Get employees
    employees = get_employee_input()
    
    if not employees:
        print("\nNo employees added. Exiting.")
        return None
    
    # Get job parameters
    params = get_job_input()
    
    # Create job
    job = FlooringJob()
    job.rooms = rooms
    job.employees = employees
    job.days_required = params['days']
    job.sanding_cost_per_sqft = params['sanding']
    job.customer_provides_wood = params['customer_provides_wood']
    job.material_cost_per_sqft = params.get('material_cost', 0.0)
    job.pickup_fee = params.get('pickup_fee', 0.0)
    
    return job


if __name__ == "__main__":
    print("\n" + "="*60)
    print("         FLOORING COST CALCULATOR")
    print("="*60)
    print("\nEnter project information to calculate total cost.")
    
    # Get input from user
    job = create_job_from_input()
    
    if job:
        # Display results
        print_cost_report(job)
        
        # Ask if they want to run another calculation
        while True:
            again = input("Would you like to calculate another job? (yes/no): ").strip().lower()
            if again in ['yes', 'y']:
                print("\n" + "="*60)
                job = create_job_from_input()
                if job:
                    print_cost_report(job)
            elif again in ['no', 'n']:
                print("\nThank you.")
                break
            else:
                print("Please enter 'yes' or 'no'.")

