from simulator import AdvancedInventorySimulator
import time

if __name__ == "__main__":
    # Use the correct relative path from LiveExpiry directory
    sim = AdvancedInventorySimulator('../shared_assets/expanded_dataset_walmart_final_priced.csv')

    # Run simulation for 5 days (you can change this to test longer periods)
    for _ in range(5):
        sim.simulate_day()
        time.sleep(200)

    # Save the updated simulation
    sim.save_simulation('../shared_assets/simulated_inventory_advanced.csv')

    # Optional: print preview
    print(sim.get_dataframe().head())
