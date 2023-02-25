PULSONIX_LIBRARY_ASCII "SamacSys ECAD Model"
//251893/1022408/2.49/3/3/Diode

(asciiHeader
	(fileUnits MM)
)
(library Library_1
	(padStyleDef "r120_65"
		(holeDiam 0)
		(padShape (layerNumRef 1) (padShapeType Rect)  (shapeWidth 0.65) (shapeHeight 1.2))
		(padShape (layerNumRef 16) (padShapeType Ellipse)  (shapeWidth 0) (shapeHeight 0))
	)
	(textStyleDef "Normal"
		(font
			(fontType Stroke)
			(fontFace "Helvetica")
			(fontHeight 1.27)
			(strokeWidth 0.127)
		)
	)
	(patternDef "SOT96P240X120-3N" (originalName "SOT96P240X120-3N")
		(multiLayer
			(pad (padNum 1) (padStyleRef r120_65) (pt -1.05, 0.96) (rotation 90))
			(pad (padNum 2) (padStyleRef r120_65) (pt -1.05, -0.96) (rotation 90))
			(pad (padNum 3) (padStyleRef r120_65) (pt 1.05, 0) (rotation 90))
		)
		(layerContents (layerNumRef 18)
			(attr "RefDes" "RefDes" (pt 0, 0) (textStyleRef "Normal") (isVisible True))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt -1.9 1.75) (pt 1.9 1.75) (width 0.05))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt 1.9 1.75) (pt 1.9 -1.75) (width 0.05))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt 1.9 -1.75) (pt -1.9 -1.75) (width 0.05))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt -1.9 -1.75) (pt -1.9 1.75) (width 0.05))
		)
		(layerContents (layerNumRef 28)
			(line (pt -0.65 1.45) (pt 0.65 1.45) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt 0.65 1.45) (pt 0.65 -1.45) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt 0.65 -1.45) (pt -0.65 -1.45) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt -0.65 -1.45) (pt -0.65 1.45) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt -0.65 0.49) (pt 0.31 1.45) (width 0.025))
		)
		(layerContents (layerNumRef 18)
			(line (pt -0.1 1.45) (pt 0.1 1.45) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt 0.1 1.45) (pt 0.1 -1.45) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt 0.1 -1.45) (pt -0.1 -1.45) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -0.1 -1.45) (pt -0.1 1.45) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -1.65 1.535) (pt -0.45 1.535) (width 0.2))
		)
	)
	(symbolDef "DMG2305UX-13" (originalName "DMG2305UX-13")

		(pin (pinNum 1) (pt 0 mils 0 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -25 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 2) (pt 0 mils -100 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -125 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 3) (pt 800 mils 0 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 570 mils -25 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(line (pt 200 mils 100 mils) (pt 600 mils 100 mils) (width 6 mils))
		(line (pt 600 mils 100 mils) (pt 600 mils -200 mils) (width 6 mils))
		(line (pt 600 mils -200 mils) (pt 200 mils -200 mils) (width 6 mils))
		(line (pt 200 mils -200 mils) (pt 200 mils 100 mils) (width 6 mils))
		(attr "RefDes" "RefDes" (pt 650 mils 300 mils) (justify Left) (isVisible True) (textStyleRef "Normal"))
		(attr "Type" "Type" (pt 650 mils 200 mils) (justify Left) (isVisible True) (textStyleRef "Normal"))

	)
	(compDef "DMG2305UX-13" (originalName "DMG2305UX-13") (compHeader (numPins 3) (numParts 1) (refDesPrefix D)
		)
		(compPin "1" (pinName "G") (partNum 1) (symPinNum 1) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "2" (pinName "S") (partNum 1) (symPinNum 2) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "3" (pinName "D") (partNum 1) (symPinNum 3) (gateEq 0) (pinEq 0) (pinType Unknown))
		(attachedSymbol (partNum 1) (altType Normal) (symbolName "DMG2305UX-13"))
		(attachedPattern (patternNum 1) (patternName "SOT96P240X120-3N")
			(numPads 3)
			(padPinMap
				(padNum 1) (compPinRef "1")
				(padNum 2) (compPinRef "2")
				(padNum 3) (compPinRef "3")
			)
		)
		(attr "Manufacturer_Name" "Diodes Inc.")
		(attr "Manufacturer_Part_Number" "DMG2305UX-13")
		(attr "Mouser Part Number" "621-DMG2305UX-13")
		(attr "Mouser Price/Stock" "https://www.mouser.co.uk/ProductDetail/Diodes-Incorporated/DMG2305UX-13?qs=L1DZKBg7t5Hgw5KN3G2IRg%3D%3D")
		(attr "Arrow Part Number" "DMG2305UX-13")
		(attr "Arrow Price/Stock" "https://www.arrow.com/en/products/dmg2305ux-13/diodes-incorporated?region=nac")
		(attr "Mouser Testing Part Number" "")
		(attr "Mouser Testing Price/Stock" "")
		(attr "Description" "MOSFET P-Ch 20V 5A Enhancement SOT23 Diodes Inc DMG2305UX-13 P-channel MOSFET Transistor, -3.3 A, -20 V, 3-Pin SOT-23")
		(attr "<Hyperlink>" "https://componentsearchengine.com/Datasheets/2/DMG2305UX-13.pdf")
		(attr "<Component Height>" "1.2")
		(attr "<STEP Filename>" "DMG2305UX-13.stp")
		(attr "<STEP Offsets>" "X=0;Y=0;Z=0")
		(attr "<STEP Rotation>" "X=0;Y=0;Z=0")
	)

)
