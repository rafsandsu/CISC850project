import random
import math
from datetime import datetime, timedelta
from dia2 import gen_sample

glucose_dose_codes = {48, 57, 58, 59, 60, 61, 62, 63, 64}
pre_meal_glucose={58, 60, 62, 64}
post_meal_glucose={59, 61, 63}
Hypoglycemic_symptoms=[65]

def jamming_attacks(samples):
    samples_w_jamming = {}

    for day in samples.keys():
        samples_w_jamming[day] = {}

        for time in samples[day]:
            samples_w_jamming[day][time] = samples[day][time].copy()
            entries = samples[day][time]

            for entry in entries:

                if entry["code"] in glucose_dose_codes:
                    samples_w_jamming[day][time].append({
                        "code": entry["code"],
                        "value": 0, #jamming the glucose monitor, all the glucose values will be set to zero
                        "label":'G'
                    })

    return samples_w_jamming

def impersonationattacks_premeal(samples):
    samples_w_attack = {}
    for day in samples.keys():
        samples_w_attack[day] = {}

        for time in samples[day]:
            samples_w_attack[day][time] = samples[day][time].copy()
            entries = samples[day][time]

            for entry in entries:
                if entry["code"] in pre_meal_glucose:
                    samples_w_attack[day][time].append({
                        "code": entry["code"],
                        "value": random.randint(300,500), #impersonating the pre meal glucose reading from the random values between 300 and 500
                        "label": 'G'
                    })

    return samples_w_attack

def impersonationattacks_postmeal(samples):
    samples_w_attack = {}
    for day in samples.keys():
        samples_w_attack[day] = {}

        for time in samples[day]:
            samples_w_attack[day][time] = samples[day][time].copy()
            entries = samples[day][time]

            for entry in entries:

                if entry["code"] in post_meal_glucose:
                    samples_w_attack[day][time].append({
                        "code": entry["code"],
                        "value": random.randint(1,50), #impersonating the post meal glucose reading from the random values between 1 and 50
                        "label": 'G'
                    })

    return samples_w_attack

def hypoglycemic(samples):
    samples_attack = {}
    for day in samples.keys():
        samples_attack[day] = {}

        for time in samples[day]:
            samples_attack[day][time] = samples[day][time].copy()
            entries = samples[day][time]

            for entry in entries:

                if entry["code"] in Hypoglycemic_symptoms  :
                    samples_attack[day][time].append({
                        "code": 65,
                        "value": random.randint(140,170), #impersonating normal readings for hypoglycemic patients
                        "label": 'G'
                    })

    return samples_attack


def replayattacks_premeal(glucose_packet, samples):
    samples_w_replay = {}
    for day in samples.keys():
        samples_w_replay[day] = {}

        for time in samples[day]:
            samples_w_replay[day][time] = samples[day][time].copy()
            entries = samples[day][time]

            for entry in entries:
                if entry["code"] in pre_meal_glucose:
                    samples_w_replay[day][time].append({
                        "code": 58,
                        "value": 480, #replaying value 480 for packet 58
                        "label": 'G'
                    })

    return samples_w_replay
    
def gather_glucose_packets(patient_id):
    patient_id = "0"+str(patient_id) if patient_id < 10 else str(patient_id)
    patient_file = r'C:\Users\rafsa\OneDrive\Desktop\CISC 850\Diabetes-Data/data-01'.format(patient_id)

    glucose_packets = {48: [], 57: [], 58:[], 59:[], 60:[], 61:[], 62:[], 63:[], 64:[]}

    with open(patient_file) as f:
        for line in f.readlines():
            _, _, code, value = line.split('\t')

            if int(code) in glucose_dose_codes:
                glucose_packets[int(code)].append(int(float(value)))

    return glucose_packets



if __name__ == "__main__":
    patient_id = 70
    samples = gen_sample(patient_id, num_samples=None)
    jamming_samples = jamming_attacks(samples)
    glucose_packets = gather_glucose_packets(patient_id)
    impersonate_premeal= impersonationattacks_premeal(samples)
    impersonate_postmeal= impersonationattacks_postmeal(samples)
    hypoglycemic=hypoglycemic(samples)
    replay_attack= replayattacks_premeal(glucose_packets,jamming_samples) #replaying value 480 and 0 for packet 58
    print(jamming_samples)
    print(impersonate_premeal)
    print(impersonate_postmeal)
    print(replay_attack)
    print(hypoglycemic)
    print(replay_attack)
     
