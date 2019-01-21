import {ViewChild, Component, ElementRef, ViewContainerRef} from '@angular/core';
import { discoverLocalRefs } from '@angular/core/src/render3/context_discovery';

@Component ({
    selector: 'c-course',
    template: `
        <h1> Hello {{ name }}</h1>
        <input #input_url >
        <img [src]="url" *ngIf="show">
        <button (click)="onChange($event, input_url.value)">Change</button>
 
    `,
    styles: [`
        div{
            background: yellow;
        }
        div.select{
            background: red;
        }
    `]
})
export class CourseComponent {
    show = true;
    name = "Tom";
    url = "http://www.risasinmas.com/wp-content/uploads/2012/03/perro-lengua-rsm-600x600.jpg";
    list = ['Pepe, maria, juan']

    @ViewChild('input_url')
    input_url: ElementRef;

    onChange(e, new_url){
        this.show = !this.show;
        console.log(this.input_url);
        this.url = new_url;
        this.name = `${this.name}A`;
        
    }

}