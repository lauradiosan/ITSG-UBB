import { Component, Input } from '@angular/core';

@Component({
  selector: 'cross-loader',
  templateUrl: './cross-loader.component.html',
  styleUrls: ['./cross-loader.component.scss']
})
export class CrossLoaderComponent { 
  @Input() showText: Boolean = true;
  @Input() whiteBackground: Boolean = true;
}