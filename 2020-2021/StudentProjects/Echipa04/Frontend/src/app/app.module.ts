import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TransformTextPipe } from './shared/pipes/transform-text.pipe';
import { LandingPageComponent } from './components/landing-page/landing-page.component';
import { NavBarComponent } from './components/nav-bar/nav-bar.component';
import { AnalysisPageComponent } from './components/analysis-page/analysis-page.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSelectModule } from '@angular/material/select';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { MedicalImageViewerComponent } from './components/medical-image-viewer/medical-image-viewer.component';
import { ToastrModule } from 'ngx-toastr';
import { CrossLoaderComponent } from './components/cross-loader/cross-loader.component';
import { LoginRegisterComponent } from './components/login-register/login-register.component';
import {MatTooltipModule} from '@angular/material/tooltip';
import { TransformIconPipe } from './shared/pipes/transform-icon.pipe';
import { NgxSliderModule } from '@angular-slider/ngx-slider';
import { SafeHtmlPipe } from './shared/pipes/safeHtml.pipe';
import { HistoryComponent } from './components/history/history.component';
import {MatTableModule} from '@angular/material/table';

@NgModule({
  declarations: [
    AppComponent,
    TransformTextPipe,
    TransformIconPipe,
    SafeHtmlPipe,
    LandingPageComponent,
    NavBarComponent,
    AnalysisPageComponent,
    DashboardComponent,
    MedicalImageViewerComponent,
    CrossLoaderComponent,
    LoginRegisterComponent,
    HistoryComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AppRoutingModule,
    BrowserModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatSelectModule,
    BrowserAnimationsModule,
    NgxSliderModule,
    MatTableModule,
    MatProgressSpinnerModule,
    ToastrModule.forRoot({
      preventDuplicates: true
    }),
    MatTooltipModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
