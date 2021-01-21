import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class HomeGuestService {

  constructor(private http: HttpClient) {
  }
}
