import { Pipe, PipeTransform } from '@angular/core';
import { ICONS } from '../assets/icons';
import { DomSanitizer } from '@angular/platform-browser';

@Pipe({ name: 'transformIcon' })
export class TransformIconPipe implements PipeTransform {
    constructor(private sanitizer: DomSanitizer) { }

    transform(value: string): any {
        if (value)
            return this.sanitizer.bypassSecurityTrustHtml(ICONS[value]) || '';
    }
}