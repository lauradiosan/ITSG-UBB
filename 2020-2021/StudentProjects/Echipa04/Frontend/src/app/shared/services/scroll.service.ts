import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ScrollService {
  constructor() { }

  scrollToElementID(elementID: string) {
    let position = this.getElementPosition(elementID);
    this.scrollToPosition(position);
  }

  scrollToTop() {
      this.scrollToPosition(0);
  }

  private scrollToPosition(targetY: number) {
      const timeOut = 20;
      const scrollMargin = 32;
      let nextTarget;
      let multiplier = window.pageYOffset <= targetY ? 1 : -1;
      let speed = 0;
      let isFinalAdjustment = false;
      let currY;
      let initialY = window.pageYOffset;

      requestAnimationFrame(step);
      function step() {
          setTimeout(function () {

              nextTarget = (nextTarget || window.pageYOffset) + multiplier * (scrollMargin + 40 * speed);

              let compare = multiplier === 1 ? nextTarget < targetY : nextTarget > targetY;
              if (!compare) {
                  compare = isFinalAdjustment = true;
                  nextTarget = targetY;
              }
              if (currY !== window.pageYOffset) {
                  currY = window.pageYOffset;
                  window.scrollTo(0, nextTarget);
                  if (Math.floor(nextTarget) > window.pageYOffset)
                      isFinalAdjustment = true;
                  let y = ((currY - initialY) / (targetY - initialY)) * Math.PI;
                  speed = Math.sin(y);
                  if (!isFinalAdjustment) {
                      requestAnimationFrame(step);
                  }
              }
          }, timeOut);
      }
  }

  getElementPosition(elementID: string, offSetTopAdjustment?: number): number {
    let offsetTop = 0;
    let element = document.getElementById(elementID);

    while (element.offsetParent) {
        offsetTop += element.offsetTop;
        element = <HTMLElement>element.offsetParent;
    }

    offsetTop -= this.getNavbarHeight();

    if (offSetTopAdjustment)
        offsetTop += offSetTopAdjustment;

    return offsetTop;
  }

  private getNavbarHeight(): number {
      let navbar = document.getElementById('navbar');

      if (navbar)
          return navbar.clientHeight;

      return 0;
  }
}