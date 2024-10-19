import pandas as pd
import os
import numpy as np
import json
from Services.Services.PersonService import PersonService
from Domain.Entities.Award import Award
from Services.Services.AwardService import AwardService
from Services.Services.ValidationService import ValidationService
from Services.Services.ConnectionService import ConnectionService
from Services.Services.TransferService import TransferService
from Services.Services.ConversionService import ConversionService
from Domain.Entities.Gift import Gift
from datetime import datetime
from Domain.Entities.Calendar import Calendar
from Domain.Entities.Person import Person
from Services.Models.Results.ValidationResult import ValidationResult
from Application.Models.Request.ConversionRequestModel import ConversionRequestModel
from Domain.Entities.Conversion import Conversion
from Domain.Enums.AwardStatus import AwardStatus
from Services.Services.GiftService import GiftService
from Services.Services.DistributionService import DistributionService
from Services.Services.DashboardService import DashboardService
from Application.Models.Request.TransferRequestModel import TransferRequestModel
from Application.Models.Response.DashboardResponseModel.AccumulatedResidueResponseModel import AccumulatedResidueResponseModel
from Application.Models.Request.SchedulingRequestModel import SchedulingRequestModel
from Services.Services.CalendarService import CalendarService

"""
local_connection = ConnectionService.open_local_connection()
local_cursor = local_connection.cursor()

json_data = """
{
"PersonId": 3,
"RouletteId": 309100,
"AwardDate": "2024-09-13 22:29:00"
}

"""

# Deserializar o JSON
data = json.loads(json_data)


AwardService().distribute_gifts_to_next_day(datetime(2024, 9, 14), local_cursor)
"""

"""

"""





























