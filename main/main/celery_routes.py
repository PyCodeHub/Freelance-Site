from kombu import Exchange , Queue


default_exchenge = Exchange('default' , 'direct')
otp_exchenge = Exchange('otp' , 'direct')
project_exchenge = Exchange('project' , 'direct')
contact_exchenge = Exchange('contact' , 'direct')

task_queues = {
    Queue('default' , exchange= default_exchenge , routing_key='default'),
    Queue('otp' , exchange= otp_exchenge , routing_key='otp'),
    Queue('project' , exchange= project_exchenge , routing_key='project'),
    Queue('contact' , exchange= contact_exchenge , routing_key='contact'),
}

task_routes = {
    'accounts.tasks.expire_otps_task':{'queue':'otp'},
    'content.tasks.expire_projects_task' : {'queue':'project'},
    'content.tasks.contact_task' : {'queue':'contact'},
}

task_default_queue = 'default'
task_default_exchenge = 'default'
task_default_routing_key = 'default'






