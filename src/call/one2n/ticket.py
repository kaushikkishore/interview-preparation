"""
Train ticket price calculator

Problem statement
We want to develop a module to help IRCTC to calculate the ticket price for a given train. Idea is to give this module as an extension to different apps in future. Below are some examples

Example 1
A train number 12345 has only sleeper and general coaches. The train runs between Mumbai to Pune and it has stops as shown below
Start - Mumbai	Stop 1 - Karjat	Stop 2 - Lonavala	Stop 3 - Chinchwad	Stop 4 - Pune
Passengers can board at any stop and leave at any stop ahead.

This train follows fix-per-station pricing strategy as below

For each stop passenger has to pay

Rs. 20/- for general coach

Rs. 40/- for sleeper coach

Cases
# of passengers	Train number	Coach	Start station	End station	Total Price
1	12345	general	Karjat	Chinchwad	40/-
3	12345	sleeper	Mumbai	Pune	3 * 40 * 4 = 480/-

"""

"""

TrainDetails 
ReservationDetails 
JourneyDetails


PricingCalculator 
    - train_details 
    - reservation_details 
    - journey_details

    - Return the price 



PricingServiceInterface 
    - calculate_price(train_details, reservation_details, journey_details): return the price  # Error handling 

PricingServiceImplementation 
    
Test Cases 
#1 Valid train details are passed + valid reservation details + valid journey details 
#2 Invalid Train details are passed 
# Invalid Reservation details 
# Invalid Journey details 
# Error handling case when We are failing to calculate the price 
# Combination of first test case where either is invalid 
# 


"""

"""
models/
- TrainDetails
- ReservationDetails
- JourneyDetails



Maintain a mapiing of train number and which stations it goes throug
train_id -> which all station it goes through 
train_id - associated with a up and down train ( 2 different train numbers )

traing_going_up - from start to end 
train_going_down - from end to start 





"""
# Pydentic for validations
from pydantic import BaseModel, Field, UUID4
from typing import List


"""
entity/models/
"""


# station.py
class Station(BaseModel):
    station_position: int = Field(
        ..., description="A valid station id"
    )  # When going up this will sorted from o - n and going down it will sorted in descending order
    station_name: str = Field(..., description="A valid station name")
    station_code: str = Field(..., description="A valid station code")


# train.py
class Train(BaseModel):
    train_id: UUID4 = Field(..., description="A valid train id")
    train_direction: str = Field(..., description="A valid train direction")
    train_number: str = Field(..., description="A train number")
    stations: List[Station] = Field(
        ..., description="a list of station train is running"
    )


# class TrainDetails(BaseModel):
#     train_number: str = Field(..., description="A valid train number")


# reservation_details.py
class ReservationDetails(BaseModel):
    travel_class: str = Field(..., description="A travel class such as sleeper general")


# journey_details.py
class JourneyDetails(BaseModel):
    start_station: str = Field(..., description="A valid start station code")
    end_station: str = Field(..., description="A valid end station code")
    number_of_passengers: int = Field(
        ..., description="A valid number of passengers", min=1, max=10
    )


# price_model.py
class PriceModel(BaseModel):
    reservation_class: str = Field(..., description="A valid reservation class")
    price_per_station: int = Field(..., description="price between the stations")


class TrainPricingDetails(BaseModel):
    """
    per class pricing between stations
    """

    pricing_model: List[PriceModel] = Field(..., description="A valid pricing model")


class PricingCalculatorInput(BaseModel):
    train_number: str
    number_of_passengers: int
    start_station_code: str
    end_station_code: str
    reservation_class: str


"""
entity/interfaces/
"""
from abc import ABC, abstractmethod


# train_service.py
class TrainService(ABC):
    """
    train id will be uuid and its a key
    direction will either up or down
    """

    @abstractmethod
    def get_train_by_train_number(self, train_number: str) -> Train:
        pass


# pricing_service.py
class PricingService(ABC):
    @abstractmethod
    def get_train_pricing_details(self, train_number: str) -> TrainPricingDetails:
        pass


class TrainPricingCalculator(ABC):
    @abstractmethod
    def calculate(self, input_details: PricingCalculatorInput) -> int:
        pass


"""
implementation/core_services/
"""


# train_service_implementation.py
class TrainServiceImplementation(TrainService):
    def get_train_by_train_number(self, train_number: str) -> Train:
        pass


# pricing_service_implementation.py
class PricingServiceImplementation(PricingService):
    def get_train_pricing_details(self, train_number: str) -> TrainPricingDetails:
        pass


class TrainPricingCalculatorImplementation(TrainPricingCalculator):
    def __init__(self, train_service: TrainService, pricing_service: PricingService):
        self.__train_service = train_service
        self.__pricing_service = pricing_service

    def calculate(self, input_details: PricingCalculatorInput) -> int:
        """
        01. Get the train details based on the input of train number
        02. Get the pricing details based on the train number
        03. Calculate the price based on the above details
        04. Return the price

        """
        # 01. Get the train details
        train_details = self.__train_service.get_train_by_train_number(
            input_details.train_number
        )
        print("train details", train_details)

        # 02. Get the pricing details
        pricing_details = self.__pricing_service.get_train_pricing_details(
            input_details.train_number
        )
        print("pricing details", pricing_details)

        # Calculate the price
        # find the reservation class in the pricing details
        price_per_station = 0
        for pricing_details in pricing_details.pricing_model:
            if pricing_details.reservation_class == input_details.reservation_class:
                price_per_station = pricing_details.price_per_station
                break

        # count the station user is travelling
        start_station_position = self.__get_station_postition(
            train_details, input_details.start_station_code
        )
        end_station_position = self.__get_station_postition(
            train_details, input_details.end_station_code
        )

        # Number of strations travelled
        total_station_travelled = abs(end_station_position - start_station_position)

        # total price.
        total_price = (
            input_details.number_of_passengers
            * price_per_station
            * total_station_travelled
        )

        return total_price

    def __get_station_postition(self, train_details: Train, station_code: str) -> int:
        for train_details in train_details.stations:
            if train_details.station_code == station_code:
                return train_details.station_position

        """
        TODO: Think of the direction should this throw an error?
        """
        return -1


"""
project/service_implementation/
tests/project/service_implementation/ # Pyest 
"""