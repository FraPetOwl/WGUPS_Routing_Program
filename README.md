**Package Delivery System Simulation**

This project is a simulation of a package delivery system that leverages some data structures & algorithms to (somewhat) optimize 
delivery routes and manage package data. It uses a greedy algorithm for route selection and a hash table for package data storage.

---

## **Features**
- **Greedy Delivery Algorithm**:  
  Determines the nearest package delivery location at each step to optimize routes.
- **Self-Adjusting Hash Table**:  
  Stores package information with quick lookups, inserts, and updates.
- **Truck Management**:  
  Simulates delivery trucks, tracks their mileage, and updates delivery statuses.
- **Address Updates**:  
  Implements a package address update per project requirements
- **Distance Calculation**:  
  Reads a 2D distance matrix to calculate delivery distances efficiently.
- **Time Tracking**:  
  Logs delivery times and status updates for each package using timedelta

---

## **Technologies Used**
- **Programming Language**: Python 3.x
- **Data Structures**:  
  - Hash Table (Separate Chaining for Collision Resolution) - but not required as no collisions here  
  - Lists for managing trucks and package assignments  
- **Algorithm**: Greedy Algorithm (Nearest Neighbor approach)
- **Libraries**:  
  - `csv` for data file handling  
  - `datetime` for time tracking  

---

## **How to Run**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/package-delivery-simulation.git
   cd package-delivery-simulation
   ```

2. **Setup**:
   - Ensure Python 3.x is installed. 

3. **Project Files**:
   - **main.py**: Entry point for the simulation.
   - **package.py**: Manages package data.
   - **truck.py**: Manages truck behavior.
   - **hash.py**: Custom hash table implementation.
   - **WGUPS Distance Table.csv**: Distance matrix file.
   - **WGUPS Package File.csv**: Package data file.

4. **Run the Simulation**:
   ```bash
   python main.py
   ```

5. **Output**:  
   The program will display the delivery order, total mileage, and status updates for all packages.
   
---
## **Future Improvements**
- Implement a Minimum Spanning Tree or Simulated Annealing approach for more efficient route optimization.
- Add a graphical user interface (GUI) for visualizing delivery routes.
- Allow scalability for a larger number of trucks and packages.
  
