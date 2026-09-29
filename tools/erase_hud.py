"""Remove baked-in green HUD graphics from a photo so a Rideshare G2 overlay can sit in its place.

Usage (from the project root):
    python3 -c "from tools.erase_hud import erase; erase('look-original.webp', 'out.jpg', (200,330,1360,930))"

`box` = (x0, y0, x1, y1) around the green UI in the source image. Green pixels inside it are masked,
dilated, and refilled from a smooth polynomial fit of the surrounding background plus matched noise.
Needs: pip install pillow numpy opencv-python
"""
import numpy as np, cv2, sys
from PIL import Image
U='assets-src/'  # originals live here; run from the project root
def erase(src, out, box, dil=9, deg=3, excl=None):
    im=np.array(Image.open(U+src).convert('RGB')).astype(np.float32)
    r,g,b=im[...,0],im[...,1],im[...,2]
    green=(g-np.maximum(r,b))>14
    m=np.zeros(green.shape,np.uint8); x0,y0,x1,y1=box
    m[y0:y1,x0:x1]=green[y0:y1,x0:x1]
    m=cv2.dilate(m,np.ones((dil,dil),np.uint8))
    # fit region
    pad=60; X0,Y0,X1,Y1=max(0,x0-pad),max(0,y0-pad),min(im.shape[1],x1+pad),min(im.shape[0],y1+pad)
    yy,xx=np.mgrid[Y0:Y1,X0:X1]
    sub=im[Y0:Y1,X0:X1]; ms=m[Y0:Y1,X0:X1]>0
    ok=~ms
    if excl is not None: ok&=~excl[Y0:Y1,X0:X1]
    xn=(xx-X0)/(X1-X0); yn=(yy-Y0)/(Y1-Y0)
    terms=[xn**i*yn**j for i in range(deg+1) for j in range(deg+1-i)]
    A=np.stack([t.ravel() for t in terms],1)
    res=sub.copy()
    for c in range(3):
        v=sub[...,c].ravel(); k=ok.ravel()
        for it in range(4):
            coef,*_=np.linalg.lstsq(A[k],v[k],rcond=None)
            pred=A@coef; resid=v-pred
            s=np.std(resid[k]); k=k&(np.abs(resid)<2.5*s+1)
        noise=np.random.normal(0,min(s,4),pred.shape)
        fill=(pred+noise).reshape(ms.shape)
        ch=res[...,c]; ch[ms]=fill[ms]; res[...,c]=ch
    # feather edge
    im2=im.copy(); im2[Y0:Y1,X0:X1]=res
    Image.fromarray(np.clip(im2,0,255).astype(np.uint8)).save(out,quality=88)
    return m
