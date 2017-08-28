import math


Gamma = 0.80;
IntensityMax = 255;

"""
https://stackoverflow.com/a/14917481/7906602
/** Taken from Earl F. Glynn's web page:
* <a href="http://www.efg2.com/Lab/ScienceAndEngineering/Spectra.htm">Spectra Lab Report</a>
* */
"""
def waveLengthToRGB(Wavelength):
    Red = 0
    Green = 0
    Blue = 0

    if((Wavelength >= 380) and (Wavelength<440)):
        Red = -(Wavelength - 440) / (440 - 380);
        Green = 0.0;
        Blue = 1.0;
    elif((Wavelength >= 440) and (Wavelength<490)):
        Red = 0.0;
        Green = (Wavelength - 440) / (490 - 440);
        Blue = 1.0;
    elif((Wavelength >= 490) and (Wavelength<510)):
        Red = 0.0;
        Green = 1.0;
        Blue = -(Wavelength - 510) / (510 - 490);
    elif((Wavelength >= 510) and (Wavelength<580)):
        Red = (Wavelength - 510) / (580 - 510);
        Green = 1.0;
        Blue = 0.0;
    elif((Wavelength >= 580) and (Wavelength<645)):
        Red = 1.0;
        Green = -(Wavelength - 645) / (645 - 580);
        Blue = 0.0;
    elif((Wavelength >= 645) and (Wavelength<781)):
        Red = 1.0;
        Green = 0.0;
        Blue = 0.0;
    else:
        Red = 0.0;
        Green = 0.0;
        Blue = 0.0;

    # // Let the intensity fall off near the vision limits

    if((Wavelength >= 380) and (Wavelength<420)):
        factor = 0.3 + 0.7*(Wavelength - 380) / (420 - 380);
    elif((Wavelength >= 420) and (Wavelength<701)):
        factor = 1.0;
    elif((Wavelength >= 701) and (Wavelength<781)):
        factor = 0.3 + 0.7*(780 - Wavelength) / (780 - 700);
    else:
        factor = 0.0;


    rgb = [0, 0, 0]

    # // Don't want 0^x = 1 for x <> 0
    rgb[0] = ternary(Red==0.0, 0, (int) (IntensityMax * math.pow(Red * factor, Gamma)))
    rgb[1] = ternary(Green==0.0, 0, (int) (IntensityMax * math.pow(Green * factor, Gamma)))
    rgb[2] = ternary(Blue==0.0, 0, (int) (IntensityMax * math.pow(Blue * factor, Gamma)))

    return rgb;


"""
# https://stackoverflow.com/a/34581745/7906602
/**
 * Convert a wavelength in the visible light spectrum to a RGB color value that is suitable to be displayed on a
 * monitor
 *
 * @param wavelength wavelength in nm
 * @return RGB color encoded in int. each color is represented with 8 bits and has a layout of
 * 00000000RRRRRRRRGGGGGGGGBBBBBBBB where MSB is at the leftmost
 */
"""
def wavelengthToRGB(wavelength):
    xyz = cie1931WavelengthToXYZFit(wavelength);
    rgb = srgbXYZ2RGB(xyz);

    return rgb;

"""
/**
 * Convert XYZ to RGB in the sRGB color space
 * <p>
 * The conversion matrix and color component transfer function is taken from http://www.color.org/srgb.pdf, which
 * follows the International Electrotechnical Commission standard IEC 61966-2-1 "Multimedia systems and equipment -
 * Colour measurement and management - Part 2-1: Colour management - Default RGB colour space - sRGB"
 *
 * @param xyz XYZ values in a double array in the order of X, Y, Z. each value in the range of [0.0, 1.0]
 * @return RGB values in a double array, in the order of R, G, B. each value in the range of [0.0, 1.0]
 */
"""
def srgbXYZ2RGB(xyz):
    x = xyz[0];
    y = xyz[1];
    z = xyz[2];

    rl =  3.2406255 * x + -1.537208  * y + -0.4986286 * z;
    gl = -0.9689307 * x +  1.8757561 * y +  0.0415175 * z;
    bl =  0.0557101 * x + -0.2040211 * y +  1.0569959 * z;

    return [
            srgbXYZ2RGBPostprocess(rl),
            srgbXYZ2RGBPostprocess(gl),
            srgbXYZ2RGBPostprocess(bl)
    ]

"""
/**
 * helper function for {@link #srgbXYZ2RGB(double[])}
 */
"""
def srgbXYZ2RGBPostprocess(c):
    # // clip if c is out of range
    # c = c > 1 ? 1 : (c < 0 ? 0 : c);
    c = ternary(c > 1, 1, ternary(c < 0, 0, c))

    # // apply the color component transfer function
    #c = c <= 0.0031308 ? c * 12.92 : 1.055 * Math.pow(c, 1. / 2.4) - 0.055;
    c = ternary(c <= 0.0031308, c * 12.92, 1.055 * math.pow(c, 1. / 2.4) - 0.055)

    return c;

"""
/**
 * A multi-lobe, piecewise Gaussian fit of CIE 1931 XYZ Color Matching Functions by Wyman el al. from Nvidia. The
 * code here is adopted from the Listing 1 of the paper authored by Wyman et al.
 * <p>
 * Reference: Chris Wyman, Peter-Pike Sloan, and Peter Shirley, Simple Analytic Approximations to the CIE XYZ Color
 * Matching Functions, Journal of Computer Graphics Techniques (JCGT), vol. 2, no. 2, 1-11, 2013.
 *
 * @param wavelength wavelength in nm
 * @return XYZ in a double array in the order of X, Y, Z. each value in the range of [0.0, 1.0]
 */
"""
def cie1931WavelengthToXYZFit(wavelength):
    wave = wavelength;

    t1 = (wave - 442.0) * (ternary(wave < 442.0, 0.0624, 0.0374));
    t2 = (wave - 599.8) * (ternary(wave < 599.8, 0.0264, 0.0323));
    t3 = (wave - 501.1) * (ternary(wave < 501.1, 0.0490, 0.0382));

    x =   0.362 * math.exp(-0.5 * t1 * t1) \
        + 1.056 * math.exp(-0.5 * t2 * t2) \
        - 0.065 * math.exp(-0.5 * t3 * t3);


    t1 = (wave - 568.8) * (ternary(wave < 568.8, 0.0213, 0.0247));
    t2 = (wave - 530.9) * (ternary(wave < 530.9, 0.0613, 0.0322));

    y =   0.821 * math.exp(-0.5 * t1 * t1) + 0.286 * math.exp(-0.5 * t2 * t2);


    t1 = (wave - 437.0) * (ternary(wave < 437.0, 0.0845, 0.0278));
    t2 = (wave - 459.0) * (ternary(wave < 459.0, 0.0385, 0.0725));

    z = (
        1.217 * math.exp(-0.5 * t1 * t1)
        + 0.681 * math.exp(-0.5 * t2 * t2)
    )

    return [ x, y, z ]

def ternary(cond, true, false):
	if cond:
		return true
	else:
		return false

