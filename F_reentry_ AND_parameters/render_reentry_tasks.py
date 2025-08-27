
#!/usr/bin/env python3
import json, os, sys
from datetime import datetime

TEMPLATE_ROTATE = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo><Description>Rotate MT4 reentry profiles per persona</Description></RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>{start_boundary}</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay><DaysInterval>1</DaysInterval></ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals><Principal id="Author"><LogonType>Password</LogonType><RunLevel>HighestAvailable</RunLevel></Principal></Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings><StopOnIdleEnd>false</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle></IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>-ExecutionPolicy Bypass -File "{ps_path}" -ProfilesRoot "{profiles_root}" -ConfigRoot "{config_root}" -Symbols "{symbols}"</Arguments>
      <WorkingDirectory>{scripts_dir}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""

TEMPLATE_KPI = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo><Description>Weekly KPI snapshot for reentry analytics</Description></RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>{start_boundary}</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByWeek>
        <DaysOfWeek><{weekday} /></DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>
  </Triggers>
  <Principals><Principal id="Author"><LogonType>Password</LogonType><RunLevel>HighestAvailable</RunLevel></Principal></Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings><StopOnIdleEnd>false</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle></IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>-ExecutionPolicy Bypass -File "{ps_path}" -DbPath "{db_path}" -SQLiteExe "{sqlite_exe}" -OutDir "{out_dir}" -Symbols "{symbols}"</Arguments>
      <WorkingDirectory>{scripts_dir}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""

def main(cfg_path: str, out_dir: str):
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    symbols = ",".join(cfg["symbols"])
    paths = cfg["paths"]
    sched = cfg["scheduling"]

    # Build StartBoundary timestamps (use today's date for examples)
    today = datetime.now().strftime("%Y-%m-%d")
    rot_time = sched["profile_rotate"]["time"] + ":00"
    rot_boundary = f"{today}T{rot_time}"
    kpi_time = sched["weekly_kpi"]["time"] + ":00"
    kpi_boundary = f"{today}T{kpi_time}"
    weekday = cfg["scheduling"]["weekly_kpi"]["day"]

    rotate_xml = TEMPLATE_ROTATE.format(
        start_boundary=rot_boundary,
        ps_path=os.path.join(paths["scripts_dir"], "reentry_profile_rotate.ps1"),
        profiles_root=paths["profiles_root"],
        config_root=paths["config_root"],
        symbols=symbols,
        scripts_dir=paths["scripts_dir"],
    )
    kpi_xml = TEMPLATE_KPI.format(
        start_boundary=kpi_boundary,
        weekday=weekday,
        ps_path=os.path.join(paths["scripts_dir"], "reentry_kpi_snapshot.ps1"),
        db_path=paths["db_path"],
        sqlite_exe=paths["sqlite_exe"],
        out_dir=paths["reports_dir"],
        symbols=symbols,
        scripts_dir=paths["scripts_dir"],
    )

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "Task_ProfileRotate.xml"), "w", encoding="utf-16") as f:
        f.write(rotate_xml)
    with open(os.path.join(out_dir, "Task_KPIWeekly.xml"), "w", encoding="utf-16") as f:
        f.write(kpi_xml)
    print("Wrote Task XMLs to", out_dir)

if __name__ == "__main__":
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(cfg_path)
    cfg_path = sys.argv[1] if len(sys.argv) > 1 else "reentry_pack_config.json"
    main(cfg_path, out)
