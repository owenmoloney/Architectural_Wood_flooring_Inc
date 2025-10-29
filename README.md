# Flooring Space Calculator

A comprehensive cost calculator for hardwood floor installation projects.

## Features

### ✅ Currently Implemented:
- **Room & Obstacle Management**: Add multiple rooms with total area and obstacles (fireplaces, closets, etc.)
- **Automatic Usable Area Calculation**: Subtracts obstacle areas from total room area
- **Multiple Employee Support**: Track different employees with individual hourly rates
- **Flexible Labor Calculation**: Set number of 8-hour work days per employee
- **Material Cost Options**:
  - Customer provides wood (no material cost)
  - Company provides wood (with pickup fee)
  - Accounts for 10% waste factor on materials
- **Sanding Costs**: Per square foot rate (automatically calculated based on floor area)
- **Detailed Cost Report**: Breakdown showing all costs

## How to Use

### Run the Standard Interactive Calculator:
```bash
python3 main.py
```

### Run the Blueprint Visual Reference Mode:
```bash
python3 blueprint_mode.py
```

### Run the GUI Application:
```bash
python3 gui.py
```

Opens a desktop application with:
- 4-panel layout (Rooms, Employees, Job Details, Cost Summary)
- Real-time cost calculation
- Add/edit/remove rooms and employees
- Visual input forms
- Cost breakdown display

The blueprint mode includes:
- Display blueprint images while entering data
- Length × Width OR direct square feet entry
- Review screen before calculation
- Enhanced prompts for guided input

The program will guide you through entering:
1. **Room Information**: Name and total area for each room
2. **Obstacles**: Areas to exclude (fireplaces, closets, islands, etc.)
3. **Employee Information**: Names and hourly rates for workers
4. **Job Parameters**: Days required, sanding cost, material costs

### Example Session:
```
Enter room name: Living Room
Enter total area: 300

Enter obstacle name: Fireplace
Enter obstacle area: 20
Enter obstacle name: none

Enter employee name: John
Enter hourly rate: 35

Enter room name: done
...
```

### Program Features:
- **Multiple Rooms**: Add as many rooms as needed
- **Multiple Obstacles**: Add multiple obstacles per room (fireplaces, closets, islands, built-ins)
- **Multiple Employees**: Track different workers with individual rates
- **Flexible Material Options**: Customer provides wood OR company provides with pickup fee
- **Repeatable**: Calculate multiple jobs in one session
- **Error Handling**: Validates all numeric inputs

## What You Might Want to Add:

### Recommended Features:
1. **Different Job Difficulty Factors**: Apply multipliers for complex layouts
2. **Multiple Material Types**: Different wood types with different costs
3. **Installation Method Costs**: Glue-down, nail-down, floating floor costs
4. **Baseboard/Trim Costs**: Per linear foot installation
5. **Underlayment Costs**: For specific flooring types
6. **Disposal Fees**: Remove and dispose of old flooring
7. **Multiple Quote Options**: Compare different material/labor combinations
8. **PDF Report Generation**: Export estimates as PDFs
9. **Database Integration**: Save and retrieve past jobs
10. **Tax Calculations**: Add sales tax or other fees
11. **Payment Terms**: Track deposits, payment schedules

## Cost Calculation Breakdown:

### Material Cost:
- If customer provides wood: $0
- If company provides wood:
  - (Usable Area × 1.10) × Cost per sq ft
  - Plus pickup fee

### Sanding Cost:
- Usable Area × Sanding Cost per sq ft

### Labor Cost:
- Sum of: (Hours × Days × 8) × Hourly Rate for each employee

### Total:
Material + Labor + Sanding

## Example Output:

```
============================================================
           FLOORING PROJECT COST ESTIMATE
============================================================

📐 FLOOR SPACE:
   Total Usable Area: 580.00 sq ft

   Room Breakdown:
   • Living Room: 280.00 sq ft usable
     (Excluding 20.00 sq ft of obstacles)
   • Kitchen: 135.00 sq ft usable
     (Excluding 15.00 sq ft of obstacles)
   • Master Bedroom: 165.00 sq ft usable
     (Excluding 35.00 sq ft of obstacles)

💰 COST BREAKDOWN:
   Sanding Cost:        $580.00
     (580.00 sq ft × $1.00/sq ft)
   Labor Cost:          $1,368.00
   Material Cost:       $5,573.00

────────────────────────────────────────────────────────────
   TOTAL PROJECT COST:  $7,521.00
============================================================
```

## Requirements

- Python 3.7+ (for dataclasses support)

No external dependencies needed - uses only Python standard library.

# Architectural_Wood_flooring_Inc
