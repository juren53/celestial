class VoyagerProbe:
    def __init__(self, name, launch_date, current_distance, speed_mph):
        """
        Initialize a Voyager probe with its specific mission parameters.
        
        :param name: Name of the probe (Voyager 1 or Voyager 2)
        :param launch_date: Date of launch
        :param current_distance: Current distance from Earth in kilometers
        :param speed_mph: Heliocentric speed in miles per hour
        """
        self.name = name
        self.launch_date = launch_date
        self.current_distance = current_distance
        
        # Specific velocities for each probe
        self.speed_mph = speed_mph
        self.speed_kms = speed_mph * 0.44704 / 1000  # Convert mph to km/s
    
    def calculate_heliocentric_speed(self, unit='mph'):
        """
        Calculate the probe's speed relative to the Sun.
        
        :param unit: Unit of speed measurement (mph or kms)
        :return: Speed in specified units
        """
        if unit == 'mph':
            return self.speed_mph
        elif unit == 'kms':
            return self.speed_kms
        else:
            raise ValueError("Invalid speed unit. Choose 'mph' or 'kms'.")
    
    def calculate_years_in_space(self):
        """
        Calculate the number of years the probe has been in space.

        :return: Years in space
        """
        from datetime import datetime
        return datetime.now().year - self.launch_date
    
    def calculate_total_distance_traveled(self):
        """
        Estimate total distance traveled based on heliocentric speed.
        
        :return: Total distance in kilometers
        """
        years_in_space = self.calculate_years_in_space()
        seconds_in_year = 365.25 * 24 * 60 * 60
        
        return self.speed_kms * seconds_in_year * years_in_space
    
    def calculate_light_time(self):
        """
        Calculate the light travel time from the probe to Earth.
        
        :return: Light time in hours and minutes
        """
        speed_of_light_kms = 299_792.458  # km/s
        light_time_seconds = self.current_distance / speed_of_light_kms
        light_time_hours = light_time_seconds / 3600
        light_time_minutes = (light_time_seconds % 3600) / 60
        
        return light_time_hours, light_time_minutes

def main():
    # Create Voyager probe instances with their specific speeds
    # Voyager 1 is traveling slightly faster than Voyager 2
    voyager1 = VoyagerProbe(
        name="Voyager 1", 
        launch_date=1977, 
        current_distance=24_900_000_000,  # kilometers (Dec 2025)
        speed_mph=38_210  # miles per hour
    )
    
    voyager2 = VoyagerProbe(
        name="Voyager 2", 
        launch_date=1977, 
        current_distance=20_700_000_000,  # kilometers (Dec 2025)
        speed_mph=35_000  # miles per hour
    )
    
    # Probe 1 calculations
    print(f"{voyager1.name} Probe Details:")
    print(f"Heliocentric Speed: {voyager1.calculate_heliocentric_speed()} mph")
    print(f"Heliocentric Speed: {voyager1.calculate_heliocentric_speed('kms'):.2f} km/s")
    print(f"Years in Space: {voyager1.calculate_years_in_space()}")
    print(f"Estimated Total Distance Traveled: {voyager1.calculate_total_distance_traveled() / 1_000_000_000:.2f} billion km")
    hours, minutes = voyager1.calculate_light_time()
    print(f"Light Time from Earth: {int(hours)} hours {int(minutes)} minutes")
    
    print("\n")
    
    # Probe 2 calculations
    print(f"{voyager2.name} Probe Details:")
    print(f"Heliocentric Speed: {voyager2.calculate_heliocentric_speed()} mph")
    print(f"Heliocentric Speed: {voyager2.calculate_heliocentric_speed('kms'):.2f} km/s")
    print(f"Years in Space: {voyager2.calculate_years_in_space()}")
    print(f"Estimated Total Distance Traveled: {voyager2.calculate_total_distance_traveled() / 1_000_000_000:.2f} billion km")
    hours, minutes = voyager2.calculate_light_time()
    print(f"Light Time from Earth: {int(hours)} hours {int(minutes)} minutes")

if __name__ == "__main__":
    main()
