import { Pipe } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

@Pipe({name: 'safeHtml'})
export class SafeHtmlPipe {
  constructor(private sanitizer: DomSanitizer){}

  transform(resource) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(resource);
  }
}