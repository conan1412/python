// #This file is part of “Sistema de Gestión de Recursos Empresariales.
//Módulo Galba Web Login Screen”.
//Empresa Socialista de Capital Mixto Guardián del ALBA.
// Author Miguel Villamizar <villamizarm@guardiandelalba.pdvsa.com>
openerp.ga_access_control = function(openerp, module){
	var _t = openerp.web._t;
	var _lt = openerp.web._lt;
	var Qweb = openerp.web.qweb;

	/*add functionality when on press enter in the field identification_id*/
	openerp.ga_access_contro = openerp.web.form.FormWidget.extend(openerp.web.form.ReinitializeWidgetMixin, {
		display_name: _lt('Form'),
		view_type: 'form',
		init:function(){
			this._super.apply(this, arguments);
		},

		initialize_field: function () {
			openerp.web.form.ReinitializeWidgetMixin.initialize_field.call(this);
			var search_attrs = document.getElementsByClassName('oe_bt_search');
			search_attrs[1].onkeypress = function(event){
				var key = event.which;
				if(key==13){
					search_attrs[2].click();
				}
			};

		}
	});

	/*In the edit mode add funtionality on click 'save' activate function worked_hours_compute to calculate hours in the installations or discard activate restore to go back in the base date (change action at sign in) */
	openerp.restore = openerp.web.form.FormWidget.extend(openerp.web.form.ReinitializeWidgetMixin, {
		display_name: _lt('Form'),
		view_type: 'form',
		init:function(){
			this._super.apply(this, arguments);
		},

		initialize_field: function () {
			var self = this;
			var actions = this.field_manager.get_field_value("action");
			var search_attrs = document.getElementsByClassName('oe_form_button_cancel');
			var attrs = document.getElementsByClassName('oe_form_button_save');
			if(actions == 'sign_out'){
				var variable = this.field_manager.get_field_value("id");
			}
			attrs[0].onclick = function () {
				if(actions == 'sign_out'){
					var model = new openerp.Model('hr.attendance');
					model.call('worked_hours_compute',[variable,variable]);
				}
			}
			search_attrs[0].onclick = function () {
				if(actions == 'sign_out'){
        			var model = new openerp.Model('ga.access.control');
					model.call('restore',[variable,variable]);
				}
			}
		}
	});

	// to remove import button and checkbox in the tree views
	var instance = openerp;
	instance.web.ListViews = instance.web.ListView.include({
		init:function(){
			this._super.apply(this,arguments);
			if(this.model == 'ga.ac.irregularity.entry' || this.model == 'ga.ac.irregularity.output' || this.model == 'ga.ac.observations.entry' || this.model == 'ga.ac.observations.output' || this.model == 'ga.ac.visitant' || this.model == 'ga.ac.vehicle' || this.model == 'hr.attendance'){
				this.options.selectable = false;//Remove checkbox
				this.options.import_enabled = false;//Remove import button
			}
		},
	});
	// to hide button more
	instance.hidden = instance.web.FormView.include({
		init: function(){
			this._super.apply(this,arguments);
		},
		// If key cancel in hr.attendace come back to the after screen
		on_button_cancel: function(event) {
	        var self = this;
	        if(this.model == "hr.attendance" ){
		        if (this.can_be_discarded()) {
		            if (this.get('actual_mode') === 'create') {
		                this.trigger('history_back');
		            } else {
		                this.to_view_mode();
		                $.when.apply(null, this.render_value_defs).then(function(){
		                    self.trigger('history_back');
		                });
		            }
		        }
		        this.trigger('on_button_cancel');
		        return false;	        	
	        }
	        else{
	        	this._super(event);
	        }

    	},

		load_form:function(data){
			this._super(data);
			if(this.model == 'ga.ac.irregularity.entry' || this.model == 'ga.ac.irregularity.output' || this.model == 'ga.ac.observations.entry' || this.model == 'ga.ac.observations.output' || this.model == 'ga.ac.visitant' || this.model == 'ga.ac.vehicle' || this.model == 'hr.attendance'){
				if(this.sidebar != undefined){
					var no_share = _.reject(this.sidebar.items['other'],function(item){
		            	return item.label === _t('Share');
		            });
		            this.sidebar.items['other'] = no_share;
		            var no_embed = _.reject(this.sidebar.items['other'],function(item){
		            	return item.label === _t('Embed');
		            });
		           	this.sidebar.items['other'] = no_embed;
		            var no_duplicate = _.reject(this.sidebar.items['other'],function(item){
		            	return item.label === _t('Duplicate');
		            });
		           	this.sidebar.items['other'] = no_duplicate;
		           	if(this.model == 'ga.ac.visitant' || this.model == 'ga.ac.vehicle' || this.model == 'hr.attendance'){
			            var no_delete = _.reject(this.sidebar.items['other'],function(item){
			            	return item.label === _t('Delete');
			            });
			           	this.sidebar.items['other'] = no_delete;
		           	}
				}
			}
		},
	});

 	openerp.web.form.custom_widgets.add('Access_Control', 'openerp.ga_access_contro');
	openerp.web.form.custom_widgets.add('Restore', 'openerp.restore');

};
