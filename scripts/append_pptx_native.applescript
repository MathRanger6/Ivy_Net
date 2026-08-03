-- Append all slides from APPEND.pptx to the end of BASE.pptx (native PowerPoint).
-- Usage: osascript append_pptx_native.applescript BASE.pptx APPEND.pptx OUT.pptx
--
-- If macOS prompts to open a file, click Allow and leave PowerPoint in the foreground.

on run argv
	if (count of argv) < 3 then
		error "Usage: osascript append_pptx_native.applescript BASE.pptx APPEND.pptx OUT.pptx"
	end if

	set basePath to item 1 of argv
	set appendPath to item 2 of argv
	set outPath to item 3 of argv

	tell application "Microsoft PowerPoint"
		activate
		delay 2

		open POSIX file basePath
		delay 2
		set baseName to name of active presentation

		open POSIX file appendPath
		delay 2
		set appendName to name of active presentation
		set nAppend to count of slides of presentation appendName

		repeat with slideIdx from 1 to nAppend
			copy object slide slideIdx of presentation appendName
			paste object presentation baseName
			delay 0.5
		end repeat

		try
			close presentation appendName saving no
		end try
		save presentation baseName in POSIX file outPath
		try
			close presentation baseName saving no
		end try
	end tell
end run
