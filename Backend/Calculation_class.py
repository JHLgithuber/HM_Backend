import Backend.mgmt_class as mgmt_class
import datetime

class Calculation:
    def __init__(self, server):
        self.server = server

    def fetch_data(self, user_id, name_of_data):
        # mgmt_class를 사용하여 데이터베이스에서 데이터를 가져옴
        mgmt_instance = mgmt_class.Mgmt(id=user_id, curd='read', entity=name_of_data, where=None, option=None, server=self.server, permission='required_permission')
        data = mgmt_instance.standard_read_ALL().result
        return data

    def calculate_water_bill(self, consumption):
        unit_price_water = 630  # 상수도 사용량 단가 (원/m³)
        water_fee_base = 850  # 구경별정액요금 (원)
        water_fee_usage = consumption * unit_price_water  # 상수도 사용 요금 (원)
        water_fee_total = water_fee_usage + water_fee_base  # 상수도 총 요금 (원)

        unit_price_sewer = 510  # 하수도 사용량 단가 (원/m³)
        sewer_fee_total = consumption * unit_price_sewer  # 하수도 총 요금 (원)

        unit_price_water_charge = 170  # 물 사용 부담금 단가 (원/m³)
        water_charge_fee_total = consumption * unit_price_water_charge  # 물 사용 부담금 총 요금 (원)

        total_fee = water_fee_total + sewer_fee_total + water_charge_fee_total

        return round(total_fee)

    def get_current_season(self):
        month = datetime.datetime.now().month   #현재 월을 가져옴... 수정필요
        if month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'fall'
        else:
            return 'winter'

    def calculate_heating_bill(self, pyeong, heating_usage):
        PYEONG_TO_SQUARE_METER = 3.3058
        BASIC_RATE_PER_SQUARE_METER = 52.4

        SEASON_RATES = {
            'spring': 99.51,
            'summer': 89.55,
            'fall': 104.53,
            'winter': 101.57
        }
        
        season = self.get_current_season()

        contract_area = pyeong * PYEONG_TO_SQUARE_METER
        basic_fee = contract_area * BASIC_RATE_PER_SQUARE_METER

        usage_rate = SEASON_RATES[season]
        usage_fee = heating_usage * usage_rate * 101570

        vat = (basic_fee + usage_fee) * 0.1
        total_fee = basic_fee + usage_fee + vat

        return round(total_fee)

    def calculate_gas_bill(self, consumption):
        base_rate = 1250
        energy_conversion_factor = 0.9964
        energy_content = 42.772
        unit_price = 20.7354
        usage_cost = consumption * energy_conversion_factor * energy_content * unit_price

        vat = (base_rate + usage_cost) * 0.1
        total_fee = base_rate + usage_cost + vat

        return round(total_fee)

    def calculate_electricity_bill(self, total_consumption):
        base_rate = 0
        consumption_tier1 = 0
        consumption_tier2 = 0
        consumption_tier3 = 0

        if total_consumption > 450:
            consumption_tier3 = total_consumption - 450
            consumption_tier2 = 150
            consumption_tier1 = 300
            base_rate = 7300
        elif total_consumption > 300:
            consumption_tier2 = total_consumption - 300
            consumption_tier1 = 300
            base_rate = 1600
        else:
            consumption_tier1 = total_consumption
            base_rate = 910

        weather_fee = total_consumption * 9.0
        fuel_cost = 5.0 * total_consumption

        electricity_bill = (base_rate + 
                            (consumption_tier1 * 120) + 
                            (consumption_tier2 * 214.6) + 
                            (consumption_tier3 * 307.3))
        electricity_bill += weather_fee + fuel_cost

        vat = electricity_bill / 10
        fund = electricity_bill * 3.7 / 100
        fund = fund - (fund % 10)

        total_fee = electricity_bill + vat + fund
        total_fee = total_fee - (total_fee % 10)

        return total_fee

    def calculate_and_return(self, user_id, name_of_data, calculation_type):
        data = self.fetch_data(user_id, name_of_data)
        consumption = data.get('consumption')
        pyeong = data.get('pyeong')
        heating_usage = data.get('heating_usage')
        total_consumption = data.get('total_consumption')

        if calculation_type == 'water':
            return self.calculate_water_bill(consumption)
        elif calculation_type == 'heating':
            return self.calculate_heating_bill(pyeong, heating_usage)
        elif calculation_type == 'gas':
            return self.calculate_gas_bill(consumption)
        elif calculation_type == 'electricity':
            return self.calculate_electricity_bill(total_consumption)
        else:
            raise ValueError("Invalid calculation type")
