tell application "Finder"
    tell disk "Transport Calculator"
        open
        
        -- Set the window size and position
        set the bounds of container window to {400, 100, 900, 450}
        
        -- Set the view options
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        
        -- Set icon arrangement
        set arrangement of icon view options of container window to not arranged
        
        -- Set icon size
        set icon size of icon view options of container window to 128
        
        -- Set position of the app icon
        set position of item "Transport Calculator.app" of container window to {150, 180}
        
        -- Set position of the Applications symlink
        set position of item "Applications" of container window to {350, 180}
        
        close
        open
        
        -- Wait for window to open
        delay 5
        
        -- Close the window
        close
    end tell
end tell 