on run
	set projectDir to "/Users/waiwai/Desktop/Plan"
	set backendCmd to "cd " & projectDir & "/backend && ./venv/bin/python app.py > /dev/null 2>&1 &"
	set frontendCmd to "export PATH=/opt/homebrew/bin:$PATH && cd " & projectDir & "/frontend && npm run dev > /dev/null 2>&1 &"

	set backendRunning to (do shell script "lsof -ti:5001 2>/dev/null || echo ''")

	if backendRunning is "" then
		-- Start both servers
		do shell script backendCmd
		do shell script frontendCmd

		-- Wait for servers to be ready
		delay 3

		-- Open browser
		do shell script "open http://localhost:5173"

		-- Show running dialog with Stop button
		display dialog "StudyDash is now running!" & return & return & "  Backend:   http://localhost:5001" & return & "  Frontend:  http://localhost:5173" & return & return & "The app is open in your browser." & return & "Click Stop when you're done." buttons {"Stop"} default button "Stop" with title "StudyDash" with icon note

		-- User clicked Stop
		do shell script "kill $(lsof -ti:5001) 2>/dev/null; kill $(lsof -ti:5173) 2>/dev/null; true"
		display notification "StudyDash servers stopped." with title "StudyDash"
	else
		-- Already running - show options
		set choice to button returned of (display dialog "StudyDash is already running!" & return & return & "What would you like to do?" buttons {"Open Browser", "Stop Servers", "Cancel"} default button "Open Browser" with title "StudyDash" with icon note)

		if choice is "Open Browser" then
			do shell script "open http://localhost:5173"
		else if choice is "Stop Servers" then
			do shell script "kill $(lsof -ti:5001) 2>/dev/null; kill $(lsof -ti:5173) 2>/dev/null; true"
			display notification "StudyDash servers stopped." with title "StudyDash"
		end if
	end if
end run
