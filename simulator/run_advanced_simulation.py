from simulator import AdvancedInventorySimulator
import time

if __name__ == "__main__":
    sim = AdvancedInventorySimulator('shared_assets/expanded_dataset_walmart_final_priced.csv')


    spreadsheet_id = '1bpKO6Zo8ce8iVykC7TSWwteSFYujJBJY1wv2hffHcMI'

    for _ in range(1):  # Simulate 5 days
        sim.simulate_day()
        # time.sleep(200)
        sim.push_to_google_sheet(spreadsheet_id)
    
    sim.save_simulation('shared_assets/simulated_inventory_advanced.csv')
    print(sim.get_dataframe().head())
