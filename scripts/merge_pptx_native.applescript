-- Merge PowerPoint decks in order (Mac + Microsoft PowerPoint).
-- Usage: osascript merge_pptx_native.applescript OUT.pptx PART1.pptx PART2.pptx ...
--
-- PART1 slides come first; slides from PART2..N are appended in order.
-- If macOS prompts to open a file, click Allow and leave PowerPoint in the foreground.

on run argv
	if (count of argv) < 2 then
		error "Usage: osascript merge_pptx_native.applescript OUT.pptx PART1.pptx [PART2 ...]"
	end if

	set outPosix to item 1 of argv
	set partPaths to rest of argv

	tell application "Microsoft PowerPoint"
		activate
		delay 2

		open POSIX file (item 1 of partPaths)
		delay 2
		set masterName to name of active presentation

		repeat with partIdx from 2 to count of partPaths
			set srcPath to item partIdx of partPaths
			open POSIX file srcPath
			delay 2
			set srcName to name of active presentation
			set nSlides to count of slides of presentation srcName

			repeat with slideIdx from 1 to nSlides
				copy object slide slideIdx of presentation srcName
				paste object presentation masterName
				delay 0.5
			end repeat

			try
				close presentation srcName saving no
			end try
		end repeat

		save presentation masterName in POSIX file outPosix
		try
			close presentation masterName saving no
		end try
	end tell
end run
