on run
	set projectDir to "/Users/waiwai/Desktop/Plan"
	set launcherScript to projectDir & "/start-app.sh"

	set backendRunning to do shell script "lsof -ti:5001 2>/dev/null || true"

	if backendRunning is "" then
		-- Not running: start everything
		try
			do shell script "bash " & quoted form of launcherScript & " 2>&1"
		on error errMsg
			display dialog "Failed to start StudyDash:" & return & return & errMsg buttons {"OK"} default button "OK" with title "StudyDash" with icon stop
			return
		end try

		-- Wait for backend to be ready (poll up to 15 seconds)
		set ready to false
		repeat 15 times
			try
				do shell script "curl -s -o /dev/null -w '%{http_code}' http://localhost:5001/ 2>/dev/null | grep -q '200\\|404\\|302'"
				set ready to true
				exit repeat
			end try
			delay 1
		end repeat

		if not ready then
			display dialog "Servers are starting but taking longer than expected." & return & "Try opening http://localhost:5173 in your browser manually." buttons {"OK"} default button "OK" with title "StudyDash" with icon caution
			return
		end if

		do shell script "open http://localhost:5173"

		display dialog "StudyDash is running!" & return & return & "  Backend:   http://localhost:5001" & return & "  Frontend:  http://localhost:5173" & return & return & "The app is open in your browser." & return & "Click Stop when you're done." buttons {"Stop"} default button "Stop" with title "StudyDash" with icon note

		-- User clicked Stop
		do shell script "kill $(lsof -ti:5001) 2>/dev/null; kill $(lsof -ti:5173) 2>/dev/null; true"
		display notification "StudyDash servers stopped." with title "StudyDash"
	else
		-- Already running
		set choice to button returned of (display dialog "StudyDash is already running!" & return & return & "What would you like to do?" buttons {"Open Browser", "Stop Servers", "Cancel"} default button "Open Browser" with title "StudyDash" with icon note)

		if choice is "Open Browser" then
			do shell script "open http://localhost:5173"
		else if choice is "Stop Servers" then
			do shell script "kill $(lsof -ti:5001) 2>/dev/null; kill $(lsof -ti:5173) 2>/dev/null; true"
			display notification "StudyDash servers stopped." with title "StudyDash"
		end if
	end if
end run
