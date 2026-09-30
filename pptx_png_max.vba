Sub MaximizeImagesKeepRatio()
    Dim sld As Slide
    Dim shp As Shape
    Dim sWidth As Single, sHeight As Single
    
    sWidth = ActivePresentation.PageSetup.SlideWidth
    sHeight = ActivePresentation.PageSetup.SlideHeight
    
    For Each sld In ActivePresentation.Slides
        For Each shp In sld.Shapes
            If shp.Type = msoPicture Or shp.Type = msoLinkedPicture Then
                With shp
                    .LockAspectRatio = msoTrue ' Keeps image proportions intact
                    
                    ' Scale based on which dimension hits the slide boundary first
                    If (.Width / .Height) > (sWidth / sHeight) Then
                        .Width = sWidth
                        .Top = (sHeight - .Height) / 2 ' Center vertically
                        .Left = 0
                    Else
                        .Height = sHeight
                        .Left = (sWidth - .Width) / 2 ' Center horizontally
                        .Top = 0
                    End If
                End With
                Exit For
            End If
        Next shp
    Next sld
    MsgBox "All images maximized proportionally!", vbInformation
End Sub