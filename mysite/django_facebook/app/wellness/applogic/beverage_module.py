import food_beverage_module

FoodAndBeverage=food_beverage_module.FoodAndBevarage

class BeverageConsumption(FoodAndBeverage):
    
    def updateBeverage(self,composition,beverage_type):
        self.composition=composition 
        self.beverage_type=beverage_type
                
    def storeFoodAndBevarageConsumption(self):
        pass
               
               
    def viewFoodAndBeverageConsumption(self):
        print(self.date_consumed)
        print(self.time_consumed)
        print(self.beneficiary_id)
        print(self.composition)       
                   
    def drawChart(self):
        pass   
            
mysnack=BeverageConsumption('12 March 2013','12:00 AM', 'Ntwa')
mysnack.updateBeverage('Soft Drink','Random')
mysnack.viewFoodAndBeverageConsumption()    
