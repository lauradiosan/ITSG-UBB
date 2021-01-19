import { Pipe, PipeTransform } from '@angular/core';
import { TEXT } from '../assets/text';

@Pipe({ name: 'transformText' })
export class TransformTextPipe implements PipeTransform {
    transform(value: string): any {
        if (value)
            return TEXT[value] || '';
    }
}