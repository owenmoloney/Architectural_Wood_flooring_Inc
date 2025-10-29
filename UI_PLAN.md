# UI Design Plan for Flooring Calculator

## UI Technology Options

### Option 1: Desktop GUI (Tkinter)
**Pros:**
- Simple, built into Python (no extra dependencies)
- Professional desktop app feel
- Easy installation (just run the file)
- Good for single-computer use

**Cons:**
- Not accessible from multiple devices
- Limited modern UI styling

### Option 2: Web Interface (Flask/FastAPI)
**Pros:**
- Accessible from any device on network
- Modern, responsive design possible
- Can run on company server
- Easy to update

**Cons:**
- Requires web server setup
- More complex than desktop GUI

### Option 3: Simple Web App (Single HTML file)
**Pros:**
- No server needed
- Simple to use
- Easy to share

**Cons:**
- Limited functionality
- No backend processing

**RECOMMENDATION: Start with Tkinter Desktop GUI**
- Easiest to build and deploy
- Professional enough for company use
- Can upgrade to web later if needed

---

## UI Layout Design

### Main Window Structure

```
┌─────────────────────────────────────────────────────────┐
│  Flooring Cost Calculator           [Blueprint Mode]     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐  ┌─────────────────────────────┐ │
│  │  ROOMS           │  │  JOB DETAILS                 │ │
│  │                  │  │                              │ │
│  │  [Room List]     │  │  Days: [___]                │ │
│  │  + Add Room      │  │  Sanding: $[___]/sq ft      │ │
│  │                  │  │                              │ │
│  │  Room details:    │  │  Material:                   │ │
│  │  [Name]: [___]   │  │  ☐ Customer provides wood   │ │
│  │  Area: [___]     │  │  ☐ Company provides         │ │
│  │  [Obstacles]     │  │     Cost: $[___]/sq ft      │ │
│  │                  │  │     Pickup: $[___]          │ │
│  └──────────────────┘  └─────────────────────────────┘ │
│                                                          │
│  ┌──────────────────┐  ┌─────────────────────────────┐ │
│  │  EMPLOYEES       │  │  COST SUMMARY                │ │
│  │                  │  │                              │ │
│  │  [Employee List] │  │  Total Floor Space:          │ │
│  │  + Add Employee │  │  [_____] sq ft               │ │
│  │                  │  │                              │ │
│  │  Name: [___]    │  │  Sanding Cost: $[_____]      │ │
│  │  Rate: $[___]/hr│  │  Labor Cost: $[_____]       │ │
│  │                  │  │  Material Cost: $[_____]    │ │
│  │                  │  │  ─────────────────────      │ │
│  │                  │  │  TOTAL: $[_____]            │ │
│  │                  │  │                              │ │
│  │                  │  │  [Calculate] [Save] [Print] │ │
│  └──────────────────┘  └─────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Detailed UI Components

### Section 1: Rooms Panel
- **Room List**: Scrollable list showing all added rooms
- **Add Room Button**: Opens room entry form
- **Room Entry Form** (popup or inline):
  - Room name (text field)
  - Area input method toggle:
    - Radio: "Length × Width" or "Total Square Feet"
  - If L×W: Two fields (Length, Width)
  - If Total: One field (Square Feet)
  - Obstacles section:
    - List of obstacles with area
    - "Add Obstacle" button
    - Obstacle name and area fields
  - Show calculated usable area (auto-updates)
  - "Save Room" and "Cancel" buttons

### Section 2: Employees Panel
- **Employee List**: Shows name and hourly rate
- **Add Employee Button**: Opens employee form
- **Employee Form**:
  - Name (text field)
  - Hourly Rate (number field)
  - "Save" and "Cancel" buttons
- Each employee row has "Edit" and "Delete" buttons

### Section 3: Job Details Panel
- **Days Required**: Number input (must be > 0)
- **Sanding Cost per sq ft**: Currency input
- **Material Options**: Radio buttons
  - "Customer provides wood" (disables material fields)
  - "Company provides wood" (enables material fields)
- **Material Cost per sq ft**: Currency input (enabled/disabled)
- **Pickup/Delivery Fee**: Currency input (enabled/disabled)

### Section 4: Cost Summary Panel
- **Real-time Calculation**: Updates as user enters data
- **Display Fields** (read-only):
  - Total Floor Space (sq ft)
  - Sanding Cost
  - Labor Cost  
  - Material Cost
  - **Total Project Cost** (large, highlighted)
- **Action Buttons**:
  - **Calculate**: Runs full calculation
  - **Save Estimate**: Save to file (JSON/CSV)
  - **Print/Export**: Generate printable estimate

---

## Additional Features to Consider

### Phase 1 (Initial Release)
- Basic form inputs for all data
- Real-time cost calculation
- Simple, clean layout
- Basic validation (numbers only, required fields)

### Phase 2 (Enhancements)
- Blueprint viewer integration (side panel or new window)
- Save/Load estimates (JSON format)
- Printable estimate report
- Multiple estimate comparison
- History of past estimates

### Phase 3 (Advanced)
- Customer database integration
- Email estimate to customer
- PDF export
- Invoice generation
- Cost templates (save common job setups)

---

## Color Scheme & Styling
- **Professional, clean design**
- Neutral colors (grays, whites, subtle blues)
- Clear, readable fonts
- Proper spacing and padding
- Buttons clearly labeled and visible
- Error messages in red (subtle)
- Success/calculation results highlighted

---

## User Flow

1. **Start Application**
   - Main window opens
   - All fields empty

2. **Add Rooms**
   - Click "Add Room"
   - Enter room name and dimensions
   - Add obstacles if needed
   - Save room (adds to list)

3. **Add Employees**
   - Click "Add Employee"
   - Enter name and rate
   - Save (adds to list)

4. **Set Job Parameters**
   - Enter days required
   - Enter sanding cost
   - Select material option
   - Enter material costs if needed

5. **View Costs**
   - Costs auto-calculate as data is entered
   - Review summary panel
   - Click "Calculate" for final totals

6. **Save/Export**
   - Click "Save Estimate" or "Print"
   - Choose file location or printer

---

## Technical Implementation Notes

### For Tkinter Version:
- Use `ttk` widgets for modern look
- Organize in frames (containers)
- Use grid layout for clean alignment
- Add tooltips for helpful hints
- Validation on inputs (only numbers, etc.)
- Error handling for edge cases

### Data Binding:
- Link UI inputs directly to FlooringJob class
- Update calculations in real-time
- Validate before calculation

### File Structure:
```
gui.py (main UI file)
  - Imports from main.py (calculation engine)
  - Contains all UI components
  - Handles user interactions
```

---

## Next Steps

1. **Choose technology** (recommend Tkinter for start)
2. **Build basic window layout** (sections in frames)
3. **Implement room input panel** (start with one section)
4. **Add calculation updates** (connect to existing code)
5. **Test with real data**
6. **Add polish** (styling, validation, error handling)
7. **Add features** (save, print, blueprint viewer)

---

## Questions to Consider

1. Will multiple people use this at once? (Web vs Desktop)
2. Do you need to save estimates to a database?
3. Should estimates be printable forms?
4. Do you want email integration?
5. Will this run on Windows, Mac, or both?

