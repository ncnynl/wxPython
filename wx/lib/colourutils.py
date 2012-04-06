"""
Some useful colour-related utility functions.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id:  $"
__revision__ = "$Revision:  $"

import wx

# Used on OSX to get access to carbon api constants
if wx.Platform == '__WXMAC__':
    try:
        import Carbon.Appearance
    except ImportError:
        CARBON = False
    else:
        CARBON = True

#-----------------------------------------------------------------------------#

def AdjustAlpha(colour, alpha):
    """Adjust the alpha of a given colour"""
    return wx.Colour(colour.Red(), colour.Green(), colour.Blue(), alpha)


def AdjustColour(color, percent, alpha=wx.ALPHA_OPAQUE):
    """
    Brighten/Darken input colour by percent and adjust alpha
    channel if needed. Returns the modified color.
    
    :param `color`: color object to adjust
    :type color: `wx.Colour`
    :param integer `percent`: percent to adjust +(brighten) or -(darken)
    :keyword `alpha`: amount to adjust alpha channel

    """
    radj, gadj, badj = [ int(val * (abs(percent) / 100.))
                         for val in color.Get() ]

    if percent < 0:
        radj, gadj, badj = [ val * -1 for val in [radj, gadj, badj] ]
    else:
        radj, gadj, badj = [ val or 255 for val in [radj, gadj, badj] ]

    red = min(color.Red() + radj, 255)
    green = min(color.Green() + gadj, 255)
    blue = min(color.Blue() + badj, 255)
    return wx.Colour(red, green, blue, alpha)


def BestLabelColour(color, bw=False):
    """
    Get the best color to use for the label that will be drawn on
    top of the given color.
    
    :param `color`: background color that text will be drawn on
    :keyword `bw`: If True, only return black or white
    
    """
    avg = sum(color.Get()) / 3
    if avg > 192:
        txt_color = wx.BLACK
    elif avg > 128:
        if bw: txt_color = wx.BLACK
        else: txt_color = AdjustColour(color, -95)
    elif avg < 64:
        txt_color = wx.WHITE
    else:
        if bw: txt_color = wx.WHITE
        else: txt_color = AdjustColour(color, 95)
    return txt_color

def GetHighlightColour():
    """Get the default highlight color
    
    :return: `wx.Colour`

    """
    if wx.Platform == '__WXMAC__':
        if CARBON:
            if wx.VERSION < (2, 9, 0, 0, ''):
                # kThemeBrushButtonPressedLightHighlight
                brush = wx.Brush(wx.BLACK)
                brush.MacSetTheme(Carbon.Appearance.kThemeBrushFocusHighlight)
                return brush.GetColour()
            else:
                color = wx.MacThemeColour(Carbon.Appearance.kThemeBrushFocusHighlight)
                return color

    # Fallback to text highlight color
    return wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
