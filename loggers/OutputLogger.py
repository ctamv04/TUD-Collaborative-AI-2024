import os, requests
import sys
import csv
import glob
import pathlib

def output_logger(fld):
    recent_dir = max(glob.glob(os.path.join(fld, '*/')), key=os.path.getmtime)
    recent_dir = max(glob.glob(os.path.join(recent_dir, '*/')), key=os.path.getmtime)
    action_files = glob.glob(os.path.join(recent_dir, 'world_1/action*'))
    if action_files:
        action_file = action_files[0]
    else:
        print(f"No action files found in {os.path.join(recent_dir, 'world_1')}")
        return
    action_header = []
    action_contents=[]
    trustfile_header = []
    trustfile_contents = []
    # Calculate the unique human and agent actions
    unique_agent_actions = []
    unique_human_actions = []
    with open(action_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar="'")
        for row in reader:
            if action_header==[]:
                action_header=row
                continue
            if row[2:4] not in unique_agent_actions and row[2]!="":
                unique_agent_actions.append(row[2:4])
            if row[4:6] not in unique_human_actions and row[4]!="":
                unique_human_actions.append(row[4:6])
            if row[4] == 'RemoveObjectTogether' or row[4] == 'CarryObjectTogether' or row[4] == 'DropObjectTogether':
                if row[4:6] not in unique_agent_actions:
                    unique_agent_actions.append(row[4:6])
            res = {action_header[i]: row[i] for i in range(len(action_header))}
            action_contents.append(res)

    with open(fld+'/beliefs/currentTrustBelief.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar="'")
        for row in reader:
            if trustfile_header==[]:
                trustfile_header=row
                continue
            if row:
                res = {trustfile_header[i] : row[i] for i in range(len(trustfile_header))}
                trustfile_contents.append(res)
    # Retrieve the stored trust belief values
    name3 = trustfile_contents[-1]['name']
    task3 = trustfile_contents[-1]['task']
    competence3 = trustfile_contents[-1]['competence']
    willingness3 = trustfile_contents[-1]['willingness']
    confidence3 = trustfile_contents[-1]['confidence']

    name2 = trustfile_contents[-2]['name']
    task2 = trustfile_contents[-2]['task']
    competence2 = trustfile_contents[-2]['competence']
    willingness2 = trustfile_contents[-2]['willingness']
    confidence2 = trustfile_contents[-2]['confidence']

    name = trustfile_contents[-3]['name']
    task = trustfile_contents[-3]['task']
    competence = trustfile_contents[-3]['competence']
    willingness = trustfile_contents[-3]['willingness']
    confidence = trustfile_contents[-3]['confidence']
    # Retrieve the number of ticks to finish the task, score, and completeness
    no_ticks = action_contents[-1]['tick_nr']
    score = action_contents[-1]['score']
    completeness = action_contents[-1]['completeness']
    # Save the output as a csv file
    print("Saving output...")
    with open(os.path.join(recent_dir,'world_1/output.csv'),mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['completeness','score','no_ticks','agent_actions','human_actions'])
        csv_writer.writerow([completeness,score,no_ticks,len(unique_agent_actions),len(unique_human_actions)])
    # with open(fld + '/beliefs/allTrustBeliefs.csv', mode='a+') as csv_file:
    #     csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     csv_writer.writerow([name,competence,willingness])
    with open(fld + '/beliefs/allTrustBeliefs.csv', mode='r') as csv_file:

        data = csv_file.readlines()
        index1 = -1
        index2 = -1
        index3 = -1
        i = 0
        for line in data:
            fields = line.split(';')
            if fields[0] == name: 
                if fields[1] == 'search':
                    index1 = i
                if fields[1] == 'rescue':
                    index2 = i
                if fields[1] == 'remove':
                    index3 = i
            i += 1

        if index1 == -1:
            data.append(name + ';' + task + ';' + competence + ';' + willingness + ';' + confidence + '\n')
        else:
            data[index1] = name + ';' + task + ';' + competence + ';' + willingness + ';' + confidence + '\n'

        if index2 == -1:
            data.append(name2 + ';' + task2 + ';' + competence2 + ';' + willingness2 + ';' + confidence2 + '\n')
        else:
            data[index2] = name2 + ';' + task2 + ';' + competence2 + ';' + willingness2 + ';' + confidence2 + '\n'

        if index3 == -1:
            data.append(name3 + ';' + task3 + ';' + competence3 + ';' + willingness3 + ';' + confidence3 + '\n')
        else:
            data[index3] = name3 + ';' + task3 + ';' + competence3 + ';' + willingness3 + ';' + confidence3 + '\n'
            
    with open(fld + '/beliefs/allTrustBeliefs.csv', mode='w') as csv_file:
        csv_file.writelines(data)    