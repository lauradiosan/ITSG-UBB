import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'splitString' })
export class SplitStringPipe implements PipeTransform {

    transform(value: string): any {
        return value.split('');
    }
}