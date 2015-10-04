
name_map = {
        "image"        : "config.image",
        "image_id"     : "image",
        "container_id" : "id",
        "ports"        : "networkSettings.ports",
        "running"      : "state.running",
        "started_at"   : "state.startedat",
        "finished_at"  : "state.finishedat",
        "command"      : "config.cmd"
}

datetime_type_fields = [
    'created',
    'finished_at',
    'started_at',
]
