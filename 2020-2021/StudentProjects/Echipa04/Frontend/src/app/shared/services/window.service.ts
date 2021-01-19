import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class WindowService {
    private isSafari: boolean;
    private isChrome: boolean;
    private isIE: boolean;
    private isFirefox: boolean;

    getWindow() {
        return window;
    }

    getAppProperty(propName: string) {
        return window[propName];
    }

    setAppProperty(propName: string, value: string) {
        window[propName] = value;
    }

    navigateTo(url: string, newWindow: boolean = false) {
        if (newWindow) {
            window.open(url, '_blank');
        }
        else {
            window.location.href = url;
        }
    }

    isWebkitBrowser() {
        return this.browserIsChrome() || this.browserIsSafari() || this.browserIsFirefox();
    }

    reloadPage() {
        this.getWindow().location.reload();
    }

    public browserIsSafari(): boolean {
        if (this.isSafari === undefined)
            this.isSafari = /Safari/.test(window.navigator.userAgent) && /Apple Computer/.test(window.navigator.vendor);

        return this.isSafari;
    }

    public browserIsIE(): boolean {
        if (this.isIE === undefined)
            this.isIE = /Trident/.test(window.navigator.userAgent) || /MSIE/.test(window.navigator.userAgent);

        return this.isIE;
    }

    private browserIsChrome() {
        if (this.isChrome === undefined)
            this.isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);

        return this.isChrome;
    }

    private browserIsFirefox() {
        this.isFirefox = false;

        if (navigator.userAgent.toLowerCase().indexOf('firefox') > -1) {
            this.isFirefox = true;

            return this.isFirefox;
        }
    }

    isMobileDevice() {
        return window.innerWidth <= 570 || window.innerWidth <= 570;
    }

    isTabletDevice() {
        return window.innerWidth <= 1065 && window.innerWidth > 570;
    }

    isDesktopDevice() {
        return window.innerWidth > 1065;
    }
}