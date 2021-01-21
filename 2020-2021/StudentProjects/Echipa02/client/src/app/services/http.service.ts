import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {CookieService} from './cookie.service';

@Injectable()
export class HttpService {
  private readonly baseUrl: string;

  constructor(
    private httpClient: HttpClient,
    private cookieService: CookieService) {
      this.baseUrl = 'http://localhost:5001';
  }

  public post(endpoint: string, item: any, isMultipart: boolean = false): Observable<any> {
    return this.httpClient
      .post(`${this.baseUrl}/${endpoint}`, item, this.options(isMultipart));
  }

  public postFile(endpoint: string, file: any, isMultipart: boolean = false): Observable<any> {
    const uploadData = new FormData();
    uploadData.append('file', file, file.name);

    return this.httpClient
      .post(`${this.baseUrl}/${endpoint}`, uploadData, this.options(isMultipart));
  }

  public update(endpoint: string, id: string, item: any): Observable<any> {
    return this.httpClient
      .put(`${this.baseUrl}/${endpoint}/${id}`, item, this.options());
  }

  public read(endpoint: string, id: string = ''): Observable<any> {
    if (id !== '') {
      return this.httpClient
        .get(`${this.baseUrl}/${endpoint}/${id}`, this.options());
    } else {
      return this.httpClient
        .get(`${this.baseUrl}/${endpoint}`, this.options());
    }
  }

  public getImage(endpoint: string, id: string = ''): Observable<Blob> {
    if (id !== '') {
      return this.httpClient
        .get(`${this.baseUrl}/${endpoint}/${id}`, {...this.options(), responseType: 'blob'});
    } else {
      return this.httpClient
        .get(`${this.baseUrl}/${endpoint}`, {...this.options(), responseType: 'blob'});
    }
  }

  public list(endpoint: string): Observable<any> {
    return this.httpClient
      .get(`${this.baseUrl}/${endpoint}`, this.options());
  }

  public delete(endpoint: string, id: string): Observable<any> {
    return this.httpClient
      .delete(`${this.baseUrl}/${endpoint}/${id}`, this.options());
  }

  private options(isMultipart: boolean = false) {
    return {headers: this.headers(isMultipart) };
  }

  private headers(isMultipart: boolean = false): HttpHeaders {
    let headers = new HttpHeaders();

    const bearer = this.cookieService.getUserCookie();
    if (bearer !== '') {
      headers = headers.append('auth', `${bearer}`);
    }

    return headers;
  }


}
